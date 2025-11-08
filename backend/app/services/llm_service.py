from openai import OpenAI
from app.core.config import settings
from app.schemas import LLMGenerateRequest, LLMGenerateResponse, Ingredient
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert chef specializing in restaurant-quality recipes. 
When generating recipes, focus on professional techniques, proper seasoning, plating presentation, 
and clear instructions suitable for home cooks attempting restaurant-style dishes.

Always respond with valid JSON matching this exact schema:
{
    "title": "Recipe Name",
    "description": "Brief description highlighting what makes this restaurant-quality",
    "ingredients": [
        {"name": "ingredient name", "amount": "2", "unit": "lbs", "notes": "optional prep notes"}
    ],
    "instructions": "Detailed step-by-step instructions with technique tips",
    "prep_time": 30,
    "cook_time": 45,
    "equipment": ["cast-iron skillet", "meat thermometer"],
    "plating_notes": "Professional plating suggestions",
    "suggested_tags": ["italian", "chicken", "restaurant-style", "date-night"]
}
"""


async def generate_recipe(request: LLMGenerateRequest) -> LLMGenerateResponse:
    """Generate a recipe using OpenAI API with structured output."""

    user_prompt = f"""Generate a {request.style} recipe for: {request.prompt}
    
Servings: {request.servings}

Focus on:
- Restaurant-quality ingredients and techniques
- Proper seasoning layers
- Temperature control and timing
- Professional plating
- Equipment recommendations

Return ONLY valid JSON following the schema."""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        recipe_data = json.loads(content)

        # Convert ingredients to Pydantic models
        ingredients = [
            Ingredient(**ing)
            if isinstance(ing, dict)
            else Ingredient(name=str(ing), amount="", unit=None)
            for ing in recipe_data.get("ingredients", [])
        ]

        return LLMGenerateResponse(
            title=recipe_data.get("title", "Untitled Recipe"),
            description=recipe_data.get("description", ""),
            ingredients=ingredients,
            instructions=recipe_data.get("instructions", ""),
            prep_time=recipe_data.get("prep_time"),
            cook_time=recipe_data.get("cook_time"),
            equipment=recipe_data.get("equipment", []),
            plating_notes=recipe_data.get("plating_notes"),
            suggested_tags=recipe_data.get("suggested_tags", []),
        )
    except Exception as e:
        raise Exception(f"Failed to generate recipe: {str(e)}")


async def revise_recipe(recipe_data: dict, notes: str) -> LLMGenerateResponse:
    """Revise an existing recipe based on user notes."""

    user_prompt = f"""Revise this recipe based on the following feedback:

Current Recipe:
{json.dumps(recipe_data, indent=2)}

Feedback:
{notes}

Generate an improved version addressing the feedback. Return ONLY valid JSON following the schema."""

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        recipe_data = json.loads(content)

        ingredients = [
            Ingredient(**ing)
            if isinstance(ing, dict)
            else Ingredient(name=str(ing), amount="", unit=None)
            for ing in recipe_data.get("ingredients", [])
        ]

        return LLMGenerateResponse(
            title=recipe_data.get("title", "Untitled Recipe"),
            description=recipe_data.get("description", ""),
            ingredients=ingredients,
            instructions=recipe_data.get("instructions", ""),
            prep_time=recipe_data.get("prep_time"),
            cook_time=recipe_data.get("cook_time"),
            equipment=recipe_data.get("equipment", []),
            plating_notes=recipe_data.get("plating_notes"),
            suggested_tags=recipe_data.get("suggested_tags", []),
        )
    except Exception as e:
        raise Exception(f"Failed to revise recipe: {str(e)}")
