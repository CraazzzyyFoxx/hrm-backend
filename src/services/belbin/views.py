from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.core import enums, errors
from src.core.db import get_async_session
from src.services.auth import flows as auth_flows

from . import service

router = APIRouter(prefix="/belbin", tags=[enums.RouteTag.BELBIN])


@router.post("", response_model=schemas.BelbinRoleRead)
async def belbin_role_create(
    payload: list[schemas.BelbinCreate],
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    role = await service.create(session, user, payload)
    return schemas.BelbinRoleRead.model_validate(role, from_attributes=True)


@router.get("", response_model=schemas.BelbinRoleRead)
async def belbin_role_get(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    role = await service.get_by_user(session, user)
    if not role:
        raise errors.ApiHTTPException(
            status_code=404, detail=[errors.ApiException(msg="Belbin role not found", code="not_found")]
        )
    return schemas.BelbinRoleRead.model_validate(role, from_attributes=True)


@router.delete("")
async def belbin_role_delete(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    await service.delete_by_user(session, user)
    return None
