from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import expression as sql

from src.user import schemas

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    @classmethod
    async def create(cls, db, **kwargs):
        query = (
            sql.insert(cls)
            .values(**kwargs)
            .returning(cls.email, cls.first_name, cls.last_name, cls.password)
        )
        result = await db.execute(query)
        await db.commit()
        new = result.first()
        return schemas.UserSerialiser.from_orm(new).dict()

    @classmethod
    async def update(cls, db, id, **kwargs):
        query = (
            sql.update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.id, cls.email, cls.first_name, cls.last_name, cls.password)
        )
        result = await db.execute(query)
        await db.commit()
        updated_user = result.first()
        return schemas.UserSerialiser.from_orm(updated_user).dict()

    @classmethod
    async def get(cls, db, id):
        query = sql.select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return schemas.UserSerialiser.from_orm(user).dict()

        return None

    @classmethod
    async def get_all(cls, db):
        query = sql.select(cls)
        result = await db.execute(query)
        users = result.scalars().all()
        return [schemas.UserSerialiser.from_orm(user).dict() for user in users]

    @classmethod
    async def delete(cls, db, id):
        query = sql.delete(cls).where(cls.id == id).returning(cls.id, cls.email)
        await db.execute(query)
        await db.commit()
        return True
