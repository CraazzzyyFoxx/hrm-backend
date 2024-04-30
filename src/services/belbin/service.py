import typing

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas


async def get_by_user(session: AsyncSession, user: models.User) -> typing.Sequence[models.BelbinRole]:
    query = sa.select(models.BelbinRole).filter(models.BelbinRole.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()


async def create(session: AsyncSession, user: models.User, payload: schemas.BelbinCreate) -> models.BelbinRole:
    belbin_role = models.BelbinRole(
        user_id=user.id,
        name=payload.name,
        percent=payload.percent,
        points=payload.points,
    )
    session.add(belbin_role)
    await session.commit()
    return belbin_role


async def delete_by_user(session: AsyncSession, user: models.User) -> None:
    query = sa.delete(models.BelbinRole).filter(models.BelbinRole.user_id == user.id)
    await session.execute(query)
    await session.commit()