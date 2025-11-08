from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.models import Rating, Recipe, User
from app.schemas import RatingCreate, Rating as RatingSchema

router = APIRouter()


def get_current_user_id(db: Session = Depends(get_db)) -> int:
    """Get current user ID from auth token. TODO: Implement proper JWT auth."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.id


@router.post("/", response_model=RatingSchema)
def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Create a rating for a recipe."""

    # Verify recipe ownership
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == rating.recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Create rating
    db_rating = Rating(
        recipe_id=rating.recipe_id,
        user_id=user_id,
        score=rating.score,
        notes=rating.notes,
        cooked_date=rating.cooked_date,
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating


@router.get("/recipe/{recipe_id}", response_model=List[RatingSchema])
def list_ratings(
    recipe_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Get all ratings for a recipe."""

    # Verify recipe ownership
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ratings = (
        db.query(Rating)
        .filter(Rating.recipe_id == recipe_id)
        .order_by(Rating.created_at.desc())
        .all()
    )

    return ratings


@router.put("/{rating_id}", response_model=RatingSchema)
def update_rating(
    rating_id: int,
    score: float = None,
    notes: str = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Update a rating."""

    rating = (
        db.query(Rating)
        .filter(Rating.id == rating_id, Rating.user_id == user_id)
        .first()
    )

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if score is not None:
        rating.score = score
    if notes is not None:
        rating.notes = notes

    db.commit()
    db.refresh(rating)

    return rating


@router.delete("/{rating_id}")
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Delete a rating."""

    rating = (
        db.query(Rating)
        .filter(Rating.id == rating_id, Rating.user_id == user_id)
        .first()
    )

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()

    return {"message": "Rating deleted"}
