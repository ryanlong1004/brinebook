from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models import Tag, User
from app.schemas import TagCreate, Tag as TagSchema

router = APIRouter()


def get_current_user_id(db: Session = Depends(get_db)) -> int:
    """Get current user ID from auth token. TODO: Implement proper JWT auth."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.id


@router.post("/", response_model=TagSchema)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Create a new tag."""

    # Check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        return existing_tag

    db_tag = Tag(name=tag.name, type=tag.type)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag


@router.get("/", response_model=List[TagSchema])
def list_tags(
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """List all tags, optionally filtered by type."""

    query = db.query(Tag)

    if type:
        query = query.filter(Tag.type == type)

    tags = query.order_by(Tag.name).all()
    return tags


@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Get a specific tag."""

    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Delete a tag."""

    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()

    return {"message": "Tag deleted"}
