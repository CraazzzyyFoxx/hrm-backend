from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import schemas, models
from src.core import pagination, errors

from . import service


async def get(session: AsyncSession, user: models.User, resume_id: int) -> models.Resume:
    resume = await service.get(session, resume_id)
    if not resume:
        raise errors.ApiHTTPException(
            status_code=404,
            detail=[errors.ApiException(msg="A resume with this id does not exist.", code="not_exist")],
        )
    if resume.user_id != user.id:
        raise errors.ApiHTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[errors.ApiException(msg="You are not allowed to get this resume.", code="forbidden")],
        )
    return resume


async def get_my_resumes(
    session: AsyncSession,
    user: models.User,
    params: pagination.PaginationParams
) -> pagination.Paginated[schemas.ResumeRead]:
    resumes, total = await service.get_by_user(session, user.id, params)
    resumes_read = [schemas.ResumeRead.model_validate(resume, from_attributes=True) for resume in resumes]
    return pagination.Paginated(results=resumes_read, total=total, page=params.page, per_page=params.per_page)


async def create(
    session: AsyncSession, user: models.User, data_in: schemas.ResumeCreate
) -> schemas.ResumeRead:
    resume = await service.create(session, user, data_in)
    return schemas.ResumeRead.model_validate(resume, from_attributes=True)


async def update(
    session: AsyncSession, user: models.User, resume_id: int, data_in: schemas.ResumeUpdate
) -> schemas.ResumeRead:
    resume = await get(session, user, resume_id)
    new_resume = await service.update(session, user, resume, data_in)
    return schemas.ResumeRead.model_validate(new_resume, from_attributes=True)


async def delete(
    session: AsyncSession, user: models.User, resume_id: int
) -> schemas.ResumeRead:
    resume = await get(session, user, resume_id)
    await service.delete(session, user, resume_id)
    return schemas.ResumeRead.model_validate(resume, from_attributes=True)
