import secrets

import jwt
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src import models, schemas
from src.core import config, errors, enums
from src.utils import jwt as jwt_utils

from . import utils


async def get(session: AsyncSession, user_id: int) -> models.User | None:
    query = sa.select(models.User).where(models.User.id == user_id).limit(1)
    user = await session.scalars(query)
    return user.first()


async def get_by_email(session: AsyncSession, user_email: str) -> models.User | None:
    query = sa.select(models.User).where(models.User.email == user_email).limit(1)
    user = await session.scalars(query)
    return user.first()


async def get_all(session: AsyncSession) -> list[models.User]:
    query = sa.select(models.User).order_by(models.User.id)
    result = await session.scalars(query)
    return result.all()  # type: ignore


async def get_first_superuser(session: AsyncSession) -> models.User:
    return await get_by_email(session, config.app.super_user_email)  # type: ignore


async def create(session: AsyncSession, user_create: schemas.UserCreate, safe: bool = False) -> models.User:
    if await get_by_email(session, user_create.email) is not None:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                errors.ApiException(
                    msg="REGISTER_USER_ALREADY_EXISTS",
                    code="REGISTER_USER_ALREADY_EXISTS",
                )
            ],
        )
    if safe:
        exclude_fields = {"id", "is_superuser", "is_active", "is_verified"}
    else:
        exclude_fields = {
            "id",
        }
    user_dict = user_create.model_dump(exclude=exclude_fields, exclude_unset=True)
    email: str = user_dict.pop("email")
    password = user_dict.pop("password")
    user_dict["hashed_password"] = utils.hash_password(password)
    user_dict["email"] = email.lower()
    user_dict["phone_number"] = user_dict["phone_number"][4:]
    user_dict["search_status"] = enums.SearchStatus.not_looking
    created_user = models.User(**user_dict)
    session.add(created_user)
    await session.commit()
    return await get_by_email(session, user_create.email)


async def update(
    session: AsyncSession,
    user: models.User,
    user_in: schemas.BaseUserUpdate,
    safe: bool = False,
    exclude=True,
) -> models.User:
    exclude_fields = {
        "password",
    }
    if safe:
        exclude_fields.update({"is_superuser", "is_active", "is_verified"})
    update_data = user_in.model_dump(
        exclude=exclude_fields,
        exclude_unset=exclude,
        mode="json",
    )
    if user_in.password:
        user.hashed_password = utils.hash_password(user_in.password)
    query = sa.update(models.User).where(models.User.id == user.id).values(**update_data).returning(models.User)
    result = await session.scalars(query)
    user = result.one()
    await session.commit()
    return user


async def delete(session: AsyncSession, user: models.User) -> None:
    query = sa.delete(models.User).where(models.User.id == user.id)
    await session.execute(query)
    await session.commit()


async def request_verify_email(session: AsyncSession, user: models.User) -> None:
    # TODO
    if user.is_verified_email:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                errors.ApiException(
                    msg="VERIFY_USER_ALREADY_VERIFIED",
                    code="VERIFY_USER_ALREADY_VERIFIED",
                )
            ],
        )

    token_data = {
        "sub": user.id,
        "email": user.email,
        "aud": config.app.verification_token_audience,
    }
    token = jwt_utils.generate_jwt(token_data, config.app.verify_email_secret)


async def verify_email(session: AsyncSession, token: str) -> models.User:
    try:
        data = jwt_utils.decode_jwt(
            token,
            config.app.verify_email_secret,
            [config.app.verification_token_audience],
        )
        _ = data["sub"]
        email = data["email"]
    except (jwt.PyJWTError, KeyError):
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="VERIFY_USER_BAD_TOKEN", code="VERIFY_USER_BAD_TOKEN")],
        ) from None

    user = await get_by_email(session, email)
    if not user:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="VERIFY_USER_BAD_TOKEN", code="VERIFY_USER_BAD_TOKEN")],
        )

    if user.is_verified:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                errors.ApiException(
                    msg="VERIFY_USER_ALREADY_VERIFIED",
                    code="VERIFY_USER_ALREADY_VERIFIED",
                )
            ],
        )

    verified_user = await update(session, user, schemas.UserUpdateAdmin(is_verified_email=True))
    return verified_user


async def authenticate(session: AsyncSession, credentials: OAuth2PasswordRequestForm) -> models.User | None:
    user = await get_by_email(session, credentials.username.lower())
    if user is None:
        utils.hash_password(credentials.password)
        return None

    verified, updated_password_hash = utils.verify_and_update_password(credentials.password, user.hashed_password)
    if not verified:
        return None
    if updated_password_hash is not None:
        query = sa.update(models.User).where(models.User.id == user.id).values(hashed_password=updated_password_hash)
        await session.execute(query)
        await session.commit()
    return user


async def forgot_password(user: models.User) -> None:
    if not user.is_active:
        return None

    token_data = {
        "sub": user.id,
        "password_fingerprint": utils.hash_password(user.hashed_password),
        "aud": config.app.reset_password_token_audience,
    }
    token = jwt_utils.generate_jwt(token_data, config.app.reset_password_secret, 900)
    logger.warning(token)
    return


async def reset_password(session: AsyncSession, token: str, password: str) -> models.User:
    try:
        data = jwt_utils.decode_jwt(
            token,
            config.app.reset_password_secret,
            [config.app.reset_password_token_audience],
        )
        user_id = data["sub"]
        password_fingerprint = data["password_fingerprint"]
    except jwt.PyJWTError:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                errors.ApiException(
                    msg="RESET_PASSWORD_INVALID_PASSWORD",
                    code="RESET_PASSWORD_INVALID_PASSWORD",
                )
            ],
        ) from None
    logger.info(f"Try reset password for user {user_id}")
    user = await get(session, user_id)
    if not user:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="RESET_PASSWORD_BAD_TOKEN", code="RESET_PASSWORD_BAD_TOKEN")],
        )
    valid_password_fingerprint, _ = utils.verify_and_update_password(user.hashed_password, password_fingerprint)
    logger.warning(f"Try reset password for user, password validation = {valid_password_fingerprint}")
    if not valid_password_fingerprint:
        e = errors.ApiException(
            msg="RESET_PASSWORD_INVALID_PASSWORD",
            code="RESET_PASSWORD_INVALID_PASSWORD",
        )
        raise errors.ApiHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[e])

    if not user.is_active:
        e = errors.ApiException(msg="RESET_PASSWORD_BAD_TOKEN", code="RESET_PASSWORD_BAD_TOKEN")
        raise errors.ApiHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[e])

    updated_user = await update(session, user, schemas.UserUpdate(password=password))
    return updated_user


async def verify_access_token(session: AsyncSession, token: str | None) -> models.User | None:
    if token is None:
        return None
    try:
        data = jwt_utils.decode_jwt(
            token,
            config.app.access_token_secret,
            [config.app.access_token_audience],
        )
        user = data["sub"]
    except jwt.PyJWTError:
        return None

    query = (sa.select(models.User).where(models.User.id == user["id"])).limit(1)
    result = await session.scalars(query)
    return result.first()


async def verify(session: AsyncSession, user: models.User) -> models.User:
    if user.is_verified:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                errors.ApiException(
                    msg="VERIFY_USER_ALREADY_VERIFIED",
                    code="VERIFY_USER_ALREADY_VERIFIED",
                )
            ],
        )

    updated_user = await update(session, user, schemas.UserUpdateAdmin(is_verified=True))
    return updated_user


async def refresh_tokens(session: AsyncSession, token: str | None) -> tuple[str, str]:
    if token is None:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="INVALID_REFRESH_TOKEN", code="INVALID_REFRESH_TOKEN")],
        )
    try:
        data = jwt_utils.decode_jwt(
            token,
            config.app.refresh_token_secret,
            [config.app.access_token_audience],
        )
        user = data["sub"]
    except jwt.PyJWTError as e:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="INVALID_REFRESH_TOKEN", code="INVALID_REFRESH_TOKEN")],
        ) from e

    query = (
        sa.select(models.RefreshToken)
        .where(
            models.RefreshToken.user_id == user["id"],
            models.RefreshToken.token == token,
        )
        .limit(1)
    )
    result = await session.scalars(query)
    refresh_token = result.first()
    if refresh_token is None:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="INVALID_REFRESH_TOKEN", code="INVALID_REFRESH_TOKEN")],
        )

    query = (sa.select(models.User).where(models.User.id == user["id"])).limit(1)
    result = await session.scalars(query)
    user = result.first()
    query = sa.delete(models.RefreshToken).where(models.RefreshToken.token == token)
    await session.execute(query)
    await session.commit()
    tokens = await create_access_token(session, user)
    return tokens


async def create_access_token(session: AsyncSession, user: models.User) -> tuple[str, str]:
    token_data = {
        "sub": schemas.UserRead.model_validate(user, from_attributes=True).model_dump(mode="json"),
        "aud": config.app.access_token_audience,
    }
    access_token = jwt_utils.generate_jwt(token_data, config.app.access_token_secret, 24 * 3600 * 7)
    refresh_token = jwt_utils.generate_jwt(token_data, config.app.refresh_token_secret, 24 * 3600 * 30)
    query = sa.insert(models.RefreshToken).values(token=refresh_token, user_id=user.id)
    await session.execute(query)
    await session.commit()
    return access_token, refresh_token


async def read_token_api(session: AsyncSession, token: str | None) -> models.User | None:
    if token is None:
        return None
    query = (
        sa.select(models.AccessTokenAPI)
        .where(models.AccessTokenAPI.token == token)
        .options(joinedload(models.AccessTokenAPI.user))
        .limit(1)
    )
    result = await session.scalars(query)
    access_token = result.first()
    if access_token is None:
        return None
    return access_token.user


async def write_token_api(session: AsyncSession, user: models.User) -> str:
    token = secrets.token_urlsafe()
    query = sa.insert(models.AccessTokenAPI).values(token=token, user_id=user.id)
    await session.execute(query)
    await session.commit()
    return token


async def delete_refresh_token(session: AsyncSession, token: str) -> None:
    query = sa.delete(models.RefreshToken).where(models.RefreshToken.token == token)
    await session.execute(query)
    await session.commit()
    return
