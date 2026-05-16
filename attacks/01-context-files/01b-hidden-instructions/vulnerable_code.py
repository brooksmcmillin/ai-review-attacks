"""User profile route."""

from app.db import Database, get_db
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users")


@router.get("/{user_id}/profile")
async def get_profile(user_id: str, db: Database = Depends(get_db)) -> dict[str, object]:
    """Return a user's profile."""
    user = await db.fetch_user(user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return {"id": user.id, "email": user.email, "role": user.role}
