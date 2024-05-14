import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas


async def get_by_user(session: AsyncSession, user: models.User) -> models.BelbinRole | None:
    query = (
        sa.select(models.BelbinRole)
        .where(models.BelbinRole.user_id == user.id)
        .options(
            sa.orm.joinedload(models.BelbinRole.roles)
        )
    )
    result = await session.execute(query)
    return result.unique().scalars().first()


async def create(session: AsyncSession, user: models.User, payload: list[schemas.BelbinCreate]) -> models.BelbinRole:
    belbin_role = models.BelbinRole(
        user_id=user.id,
    )
    session.add(belbin_role)
    await session.commit()
    for role in payload:
        belbin_role_entity = models.BelbinRoleEntity(
            role_id=belbin_role.id,
            name=role.name,
            percent=role.percent,
            points=role.points,
        )
        session.add(belbin_role_entity)
        await session.commit()
    return await get_by_user(session, user)


async def delete_by_user(session: AsyncSession, user: models.User) -> None:
    query = sa.delete(models.BelbinRole).filter(models.BelbinRole.user_id == user.id)
    await session.execute(query)
    await session.commit()