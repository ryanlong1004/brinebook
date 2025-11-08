from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List, Optional, Dict, Any
from app.models import Recipe, RecipeTag, Tag, Rating
from app.schemas import Recipe as RecipeSchema


def search_recipes(
    db: Session,
    user_id: int,
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 20,
) -> List[RecipeSchema]:
    """
    Search recipes using full-text search and filters.
    """

    # Base query
    base_query = db.query(Recipe).filter(Recipe.user_id == user_id)

    # Text search
    if query:
        search_filter = or_(
            Recipe.title.ilike(f"%{query}%"),
            Recipe.description.ilike(f"%{query}%"),
            Recipe.instructions.ilike(f"%{query}%"),
        )
        base_query = base_query.filter(search_filter)

    # Apply filters
    if filters:
        if filters.get("tags"):
            tag_ids = filters["tags"]
            base_query = base_query.join(RecipeTag).filter(
                RecipeTag.tag_id.in_(tag_ids)
            )

        if filters.get("source"):
            base_query = base_query.filter(Recipe.source == filters["source"])

        if filters.get("min_rating"):
            # Subquery for average rating
            rating_subq = (
                db.query(Rating.recipe_id, func.avg(Rating.score).label("avg_rating"))
                .group_by(Rating.recipe_id)
                .subquery()
            )

            base_query = base_query.join(
                rating_subq, Recipe.id == rating_subq.c.recipe_id
            ).filter(rating_subq.c.avg_rating >= filters["min_rating"])

    # Sort by relevance (title match first, then recent)
    if query:
        base_query = base_query.order_by(
            Recipe.title.ilike(f"{query}%").desc(), Recipe.created_at.desc()
        )
    else:
        base_query = base_query.order_by(Recipe.created_at.desc())

    # Limit results
    recipes = base_query.limit(limit).all()

    # Enrich with ratings and tags
    result = []
    for recipe in recipes:
        recipe_dict = {
            "id": recipe.id,
            "user_id": recipe.user_id,
            "title": recipe.title,
            "description": recipe.description,
            "source": recipe.source,
            "instructions": recipe.instructions,
            "ingredients": recipe.ingredients,
            "servings": recipe.servings,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "equipment": recipe.equipment,
            "plating_notes": recipe.plating_notes,
            "is_public": recipe.is_public,
            "base_prompt": recipe.base_prompt,
            "created_at": recipe.created_at,
            "updated_at": recipe.updated_at,
        }

        # Get average rating
        avg_rating = (
            db.query(func.avg(Rating.score))
            .filter(Rating.recipe_id == recipe.id)
            .scalar()
        )
        rating_count = (
            db.query(func.count(Rating.id))
            .filter(Rating.recipe_id == recipe.id)
            .scalar()
        )

        recipe_dict["avg_rating"] = float(avg_rating) if avg_rating else None
        recipe_dict["rating_count"] = rating_count or 0

        # Get tags
        tags = (
            db.query(Tag).join(RecipeTag).filter(RecipeTag.recipe_id == recipe.id).all()
        )
        recipe_dict["tags"] = [
            {"id": t.id, "name": t.name, "type": t.type, "created_at": t.created_at}
            for t in tags
        ]

        # Get hero photo
        hero_photo = next((p for p in recipe.photos if p.is_hero), None)
        if not hero_photo and recipe.photos:
            hero_photo = recipe.photos[0]
        recipe_dict["hero_photo"] = hero_photo.url if hero_photo else None

        result.append(RecipeSchema(**recipe_dict))

    return result


def should_suggest_llm(results: List[RecipeSchema], query: str) -> bool:
    """
    Determine if we should suggest LLM generation based on search results.
    """
    # Suggest LLM if:
    # - No results found
    # - Less than 2 results
    # - Query looks like a generation request (contains words like "recipe for", "how to make")

    if len(results) == 0:
        return True

    if len(results) < 2:
        return True

    generation_keywords = [
        "recipe for",
        "how to make",
        "how do i",
        "generate",
        "create",
        "new",
    ]
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in generation_keywords):
        return True

    return False
