from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src import schemas
from src.core import db, enums, errors, pagination
from src.services.auth import flows as auth_flows
from src.services.auth import service as auth_service

router = APIRouter(prefix="/users", tags=[enums.RouteTag.USERS])


@router.get("/@me", response_model=schemas.UserRead)
async def get_me(user=Depends(auth_flows.current_active)):
    return schemas.UserRead(
        **user.to_dict(),
    )


@router.patch("/@me", response_model=schemas.UserRead)
async def update_me(
        user_update: schemas.UserUpdate,
        user=Depends(auth_flows.current_active),
        session=Depends(db.get_async_session),
):
    user = await auth_service.update(session, user, user_update, safe=True)
    return user


@router.post("/@me/generate-api-token")
async def generate_api_token(
        user=Depends(auth_flows.current_active_superuser),
        session=Depends(db.get_async_session),
):
    response = await auth_service.write_token_api(session, user)
    return ORJSONResponse({"access_token": response, "token_type": "bearer"})
