import typing

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src import schemas, models
from src.core import pagination


async def get(session: AsyncSession, resume_id: int) -> models.Resume | None:
    query = (
        sa.select(models.Resume)
        .where(models.Resume.id == resume_id)
        .options(
            joinedload(models.Resume.basic_information).subqueryload(models.ResumeBasicInfo.citizenship),
            joinedload(models.Resume.education),
            joinedload(models.Resume.work_experience)
        )
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_by_user(
        session: AsyncSession, user_id: int, params: pagination.PaginationParams
) -> tuple[typing.Sequence[models.Resume], int]:
    query = (
        sa.select(models.Resume)
        .where(models.Resume.user_id == user_id)
        .options(
            joinedload(models.Resume.basic_information).subqueryload(models.ResumeBasicInfo.citizenship),
            joinedload(models.Resume.education),
            joinedload(models.Resume.work_experience)
        )
    )
    query = params.apply_pagination(query)
    total_query = (
        sa.select(sa.func.count(models.Resume.id)).where(models.Resume.user_id == user_id)
    )
    total_result = await session.execute(total_query)
    result = await session.execute(query)
    return result.scalars().all(), total_result.scalar_one()


async def create(
        session: AsyncSession, user: models.User, data_in: schemas.ResumeCreate
) -> models.Resume:
    resume = models.Resume(
        user=user,
        position=data_in.position,
    )
    session.add(resume)
    await session.commit()
    return await get(session, resume.id)


async def delete(
        session: AsyncSession, user: models.User, resume_id: int
) -> None:
    query = (
        sa.delete(models.Resume).where(models.Resume.user_id == user.id, models.Resume.id == resume_id)
    )
    await session.execute(query)
    await session.commit()


async def update(
        session: AsyncSession, user: models.User, resume: models.Resume, data_in: schemas.ResumeUpdate
) -> models.Resume:
    resume.position = data_in.position

    if data_in.basic_information:
        if resume.basic_information:
            resume.basic_information.first_name = data_in.basic_information.first_name
            resume.basic_information.last_name = data_in.basic_information.last_name
            resume.basic_information.middle_name = data_in.basic_information.middle_name
            resume.basic_information.gender = data_in.basic_information.gender
            resume.basic_information.phone = data_in.basic_information.phone
            resume.basic_information.birthday = data_in.basic_information.birthday
            resume.basic_information.citizenship_id = data_in.basic_information.citizenship.id
            resume.basic_information.city = data_in.basic_information.city
        else:
            resume.basic_information = models.ResumeBasicInfo(
                first_name=data_in.basic_information.first_name,
                last_name=data_in.basic_information.last_name,
                middle_name=data_in.basic_information.middle_name,
                gender=data_in.basic_information.gender,
                phone=data_in.basic_information.phone,
                birthday=data_in.basic_information.birthday,
                citizenship_id=data_in.basic_information.citizenship.id,
                city=data_in.basic_information.city,
            )
    if data_in.education:
        if resume.education:
            resume.education.level = data_in.education.level
            resume.education.name = data_in.education.name
            resume.education.faculty = data_in.education.faculty
            resume.education.specialization = data_in.education.specialization
            resume.education.year_of_graduation = data_in.education.year_of_graduation
        else:
            resume.education = models.ResumeEducation(
                level=data_in.education.level,
                name=data_in.education.name,
                faculty=data_in.education.faculty,
                specialization=data_in.education.specialization,
                year_of_graduation=data_in.education.year_of_graduation
            )
    if data_in.work_experience:
        if resume.work_experience:
            resume.work_experience.name = data_in.education.level
            resume.work_experience.position = data_in.education.name
            resume.work_experience.description = data_in.education.faculty
            resume.work_experience.start_work_month = data_in.education.specialization
            resume.work_experience.start_work_year = data_in.education.year_of_graduation
            resume.work_experience.is_end = data_in.work_experience.is_end
        else:
            resume.work_experience = models.ResumeWorkExperience(
                name=data_in.education.level,
                position=data_in.education.name,
                description=data_in.education.faculty,
                start_work_month=data_in.education.specialization,
                start_work_year=data_in.education.year_of_graduation,
                is_end=data_in.work_experience.is_end
            )
    if resume.education and resume.basic_information and resume.work_experience:
        resume.is_public = True
    session.add(resume)
    await session.commit()
    return await get(session, resume.id)
