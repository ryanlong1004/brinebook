from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import User
from app.schemas import SearchRequest, SearchResponse, LLMGenerateRequest
from app.services.search_service import search_recipes, should_suggest_llm
from app.services.llm_service import generate_recipe

router = APIRouter()


def get_current_user_id(db: Session = Depends(get_db)) -> int:
    """Get current user ID from auth token. TODO: Implement proper JWT auth."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.id


@router.post("/", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Universal search endpoint.
    Searches internal recipes and optionally generates new ones with AI.
    """

    # Search internal recipes
    internal_results = search_recipes(
        db=db,
        user_id=user_id,
        query=request.query,
        filters=request.filters,
        limit=request.limit,
    )

    # Determine if we should suggest LLM generation
    suggest_llm = should_suggest_llm(internal_results, request.query)

    # Optionally generate LLM result
    llm_result = None
    if suggest_llm and len(internal_results) < 3:
        try:
            # Generate recipe proactively for better UX
            llm_request = LLMGenerateRequest(
                prompt=request.query, style="restaurant-style", servings=4
            )
            llm_result = await generate_recipe(llm_request)
        except Exception as e:
            # Don't fail the whole request if LLM fails
            print(f"LLM generation failed: {e}")

    return SearchResponse(
        internal_results=internal_results,
        suggest_llm=suggest_llm,
        llm_result=llm_result,
    )
