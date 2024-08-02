import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db
from src.user import models, schemas


logger = logging.getLogger(__name__)
api = APIRouter(prefix="/users")


@api.post("/", response_model=dict)
async def create_user(user: schemas.UserSchema, db: AsyncSession = Depends(db.get_db)):
    try:
        new_user = await models.User.create(db, **user.dict())
        return new_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(status_code=400, detail="User creation failed")


@api.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int, user: schemas.UserSchemaUpdate, db: AsyncSession = Depends(db.get_db)
):
    try:
        updated_user = await models.User.update(db, user_id, **user.dict())
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        raise HTTPException(status_code=400, detail="User update failed")


@api.get("/{user_id}", response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(db.get_db)):
    user = await models.User.get(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api.get("/", response_model=list)
async def get_all_users(db: AsyncSession = Depends(db.get_db)):
    users = await models.User.get_all(db)
    return users


@api.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(db.get_db)):
    user = await models.User.get(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await models.User.delete(db, user_id)
    return {"detail": "User deleted successfully"}
