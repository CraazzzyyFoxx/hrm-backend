from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.core import enums
from src.core.db import get_async_session
from src.services.auth import flows as auth_flows

from . import service

router = APIRouter(prefix="/belbin", tags=[enums.RouteTag.BELBIN])


@router.post("/", response_model=list[schemas.BelbinRoleRead])
async def belbin_role_create(
    payload: list[schemas.BelbinCreate],
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    created_roles = []
    for role in payload:
        created_roles.append(await service.create(session, user, role))
    return created_roles


@router.get("/", response_model=list[schemas.BelbinRoleRead])
async def belbin_role_get(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    roles = await service.get_by_user(session, user)
    return roles


@router.delete("/")
async def belbin_role_delete(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    await service.delete_by_user(session, user)
    return None
