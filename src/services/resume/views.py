from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas, models
from src.core import enums, pagination
from src.core.db import get_async_session
from src.services.auth import flows as auth_flows

from . import flows

router = APIRouter(prefix="/resume", tags=[enums.RouteTag.RESUME])


@router.post("", response_model=schemas.ResumeRead)
async def create_resume(
    payload: schemas.ResumeCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    return await flows.create(session, user, payload)


@router.get("", response_model=schemas.ResumeRead)
async def get_resume(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(auth_flows.current_active),
):
    return await flows.get(session, user, id)


@router.get("/my", response_model=pagination.Paginated[schemas.ResumeRead])
async def get_my_resumes(
    params: pagination.PaginationParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(auth_flows.current_active),
):
    return await flows.get_my_resumes(session, user, params)


@router.delete("", response_model=schemas.ResumeRead)
async def delete_resume(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(auth_flows.current_active)
):
    return await flows.delete(session, user, id)


@router.patch("", response_model=schemas.ResumeRead)
async def update_resume(
    id: int,
    data: schemas.ResumeUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(auth_flows.current_active)
):
    return await flows.update(session, user, id, data)
