from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src import schemas
from src.core import enums, errors
from src.core.db import get_async_session

from . import flows, service

router = APIRouter(prefix="/auth", tags=[enums.RouteTag.AUTH])


@router.post("/login")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    user = await service.authenticate(session, credentials)
    if user is None:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[errors.ApiException(msg="LOGIN_BAD_CREDENTIALS", code="LOGIN_BAD_CREDENTIALS")],
        )
    token = await service.create_access_token(session, user)
    logger.info(f"User [email={user.email}] has logged in.")
    resp = ORJSONResponse({"access_token": token[0], "token_type": "bearer"})
    resp.set_cookie("refresh_token", token[1], httponly=True)
    return resp


@router.post("/registration", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: schemas.UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    created_user = await service.create(session, user_create, safe=True)
    user = schemas.UserRead.model_validate(created_user)
    logger.info(f"User [email={user.email}] has registered.")
    return user


@router.post("/request-verify-token", status_code=status.HTTP_202_ACCEPTED)
async def request_verify_token(email: EmailStr = Body(..., embed=True), session=Depends(get_async_session)):
    try:
        user = await flows.get_by_email(session, email.lower())
        await service.request_verify_email(session, user)
    except errors.ApiHTTPException:
        pass
    return None


@router.post("/verify", response_model=schemas.UserRead)
async def verify(token: str = Body(..., embed=True), session=Depends(get_async_session)):
    user = await service.verify_email(session, token)
    return schemas.UserRead.model_validate(user, from_attributes=True)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(email: EmailStr = Body(..., embed=True), session=Depends(get_async_session)):
    try:
        user = await flows.get_by_email(session, email.lower())
        await service.forgot_password(user)
    except errors.ApiHTTPException:
        pass
    return None


@router.post("/reset-password")
async def reset_password(
    token: str = Body(...),
    password: str = Body(...),
    session=Depends(get_async_session),
):
    await service.reset_password(session, token, password)


@router.post("/refresh-token")
async def refresh_token(request: Request, session=Depends(get_async_session)):
    token = await service.refresh_tokens(session, request.cookies.get("refresh_token"))
    resp = ORJSONResponse({"access_token": token[0], "token_type": "bearer"})
    resp.set_cookie("refresh_token", token[1], httponly=True)
    return resp


@router.post("/logout")
async def logout(request: Request, user=Depends(flows.current_active), session=Depends(get_async_session)):
    await service.delete_refresh_token(session, user, request.cookies.get("refresh_token"))
    resp = ORJSONResponse({"status": "success"})
    resp.delete_cookie("refresh_token")
    return resp
