from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Photo, Recipe, User
from app.schemas import PhotoCreate, Photo as PhotoSchema
from app.services.storage_service import upload_photo, delete_photo

router = APIRouter()


def get_current_user_id(db: Session = Depends(get_db)) -> int:
    """Get current user ID from auth token. TODO: Implement proper JWT auth."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.id


@router.post("/", response_model=PhotoSchema)
async def create_photo(
    recipe_id: int,
    file: UploadFile = File(...),
    caption: str = None,
    is_hero: bool = False,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Upload a photo for a recipe."""

    # Verify recipe ownership
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Upload to S3
    try:
        file_content = await file.read()
        url = await upload_photo(file_content, file.filename, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    # If this is the hero photo, unset other hero photos
    if is_hero:
        db.query(Photo).filter(
            Photo.recipe_id == recipe_id, Photo.is_hero == True
        ).update({"is_hero": False})

    # Create photo record
    db_photo = Photo(
        recipe_id=recipe_id, user_id=user_id, url=url, caption=caption, is_hero=is_hero
    )

    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return db_photo


@router.get("/recipe/{recipe_id}", response_model=List[PhotoSchema])
def list_photos(
    recipe_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Get all photos for a recipe."""

    # Verify recipe ownership
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    photos = db.query(Photo).filter(Photo.recipe_id == recipe_id).all()
    return photos


@router.delete("/{photo_id}")
async def delete_photo_endpoint(
    photo_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Delete a photo."""

    photo = (
        db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == user_id).first()
    )

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Delete from S3
    try:
        await delete_photo(photo.url)
    except Exception as e:
        print(f"S3 deletion failed: {e}")

    db.delete(photo)
    db.commit()

    return {"message": "Photo deleted"}


@router.put("/{photo_id}/hero")
def set_hero_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Set a photo as the hero image for its recipe."""

    photo = (
        db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == user_id).first()
    )

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Unset other hero photos for this recipe
    db.query(Photo).filter(
        Photo.recipe_id == photo.recipe_id, Photo.is_hero == True
    ).update({"is_hero": False})

    # Set this as hero
    photo.is_hero = True
    db.commit()

    return {"message": "Hero photo updated"}
