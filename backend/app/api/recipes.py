from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.core.database import get_db
from app.models import Recipe, RecipeTag, Tag, Rating, User
from app.schemas import (
    RecipeCreate,
    RecipeUpdate,
    Recipe as RecipeSchema,
    LLMGenerateRequest,
    LLMGenerateResponse,
    Ingredient,
)
from app.services.llm_service import generate_recipe, revise_recipe

router = APIRouter()


def get_current_user_id(db: Session = Depends(get_db)) -> int:
    """Get current user ID from auth token. TODO: Implement proper JWT auth."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.id


@router.post("/generate", response_model=LLMGenerateResponse)
async def generate_recipe_endpoint(
    request: LLMGenerateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Generate a recipe using AI."""
    try:
        result = await generate_recipe(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=RecipeSchema)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Create a new recipe."""

    # Convert Pydantic ingredients to JSON
    ingredients_json = (
        [ing.model_dump() for ing in recipe.ingredients] if recipe.ingredients else []
    )

    db_recipe = Recipe(
        user_id=user_id,
        title=recipe.title,
        description=recipe.description,
        source=recipe.source,
        base_prompt=recipe.base_prompt,
        llm_response=recipe.llm_response,
        instructions=recipe.instructions,
        ingredients=ingredients_json,
        servings=recipe.servings,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        equipment=recipe.equipment,
        plating_notes=recipe.plating_notes,
        is_public=recipe.is_public,
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    # Add tags
    if recipe.tag_ids:
        for tag_id in recipe.tag_ids:
            recipe_tag = RecipeTag(recipe_id=db_recipe.id, tag_id=tag_id)
            db.add(recipe_tag)
        db.commit()

    return get_recipe(db_recipe.id, db, user_id)


@router.get("/", response_model=List[RecipeSchema])
def list_recipes(
    skip: int = 0,
    limit: int = 20,
    source: Optional[str] = None,
    tag_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """List all recipes for the current user."""

    query = db.query(Recipe).filter(Recipe.user_id == user_id)

    if source:
        query = query.filter(Recipe.source == source)

    if tag_ids:
        tag_id_list = [int(tid) for tid in tag_ids.split(",")]
        query = query.join(RecipeTag).filter(RecipeTag.tag_id.in_(tag_id_list))

    query = query.order_by(Recipe.created_at.desc())
    recipes = query.offset(skip).limit(limit).all()

    result = []
    for recipe in recipes:
        result.append(enrich_recipe(db, recipe))

    return result


@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Get a specific recipe."""

    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return enrich_recipe(db, recipe)


@router.put("/{recipe_id}", response_model=RecipeSchema)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Update a recipe."""

    db_recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Update fields
    update_data = recipe_update.model_dump(exclude_unset=True)

    # Handle ingredients conversion
    if "ingredients" in update_data and update_data["ingredients"]:
        update_data["ingredients"] = [
            ing.model_dump() for ing in update_data["ingredients"]
        ]

    # Handle tags
    tag_ids = update_data.pop("tag_ids", None)

    for field, value in update_data.items():
        setattr(db_recipe, field, value)

    # Update tags if provided
    if tag_ids is not None:
        # Remove existing tags
        db.query(RecipeTag).filter(RecipeTag.recipe_id == recipe_id).delete()

        # Add new tags
        for tag_id in tag_ids:
            recipe_tag = RecipeTag(recipe_id=recipe_id, tag_id=tag_id)
            db.add(recipe_tag)

    db.commit()
    db.refresh(db_recipe)

    return enrich_recipe(db, db_recipe)


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Delete a recipe."""

    db_recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()

    return {"message": "Recipe deleted"}


@router.post("/{recipe_id}/revise", response_model=LLMGenerateResponse)
async def revise_recipe_endpoint(
    recipe_id: int,
    notes: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Revise a recipe using AI based on user notes."""

    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == user_id)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_data = {
        "title": recipe.title,
        "description": recipe.description,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "equipment": recipe.equipment,
        "plating_notes": recipe.plating_notes,
    }

    try:
        result = await revise_recipe(recipe_data, notes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def enrich_recipe(db: Session, recipe: Recipe) -> RecipeSchema:
    """Enrich recipe with ratings, tags, and photos."""

    # Get average rating
    avg_rating = (
        db.query(func.avg(Rating.score)).filter(Rating.recipe_id == recipe.id).scalar()
    )
    rating_count = (
        db.query(func.count(Rating.id)).filter(Rating.recipe_id == recipe.id).scalar()
    )

    # Get tags
    tags = db.query(Tag).join(RecipeTag).filter(RecipeTag.recipe_id == recipe.id).all()

    # Use hero_photo column if present, else fallback to related photo
    hero_photo_url = recipe.hero_photo if getattr(recipe, "hero_photo", None) else None
    if not hero_photo_url:
        hero_photo = next((p for p in recipe.photos if p.is_hero), None)
        if not hero_photo and recipe.photos:
            hero_photo = recipe.photos[0]
        hero_photo_url = hero_photo.url if hero_photo else None

    # Convert ingredients back to Pydantic models
    ingredients = (
        [Ingredient(**ing) for ing in recipe.ingredients] if recipe.ingredients else []
    )

    return RecipeSchema(
        id=recipe.id,
        user_id=recipe.user_id,
        title=recipe.title,
        description=recipe.description,
        source=recipe.source,
        base_prompt=recipe.base_prompt,
        instructions=recipe.instructions,
        ingredients=ingredients,
        servings=recipe.servings,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        equipment=recipe.equipment,
        plating_notes=recipe.plating_notes,
        is_public=recipe.is_public,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at,
        avg_rating=float(avg_rating) if avg_rating else None,
        rating_count=rating_count or 0,
        tags=[
            {
                "id": t.id,
                "name": t.name,
                "type": t.type,
                "created_at": t.created_at,
            }
            for t in tags
        ],
        hero_photo=hero_photo_url,
    )
