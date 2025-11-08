from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RecipeSource(str, Enum):
    LLM = "llm"
    MANUAL = "manual"
    WEB = "web"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Recipe schemas
class Ingredient(BaseModel):
    name: str
    amount: str
    unit: Optional[str] = None
    notes: Optional[str] = None


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None
    servings: int = 4
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    equipment: Optional[List[str]] = None
    plating_notes: Optional[str] = None
    is_public: bool = False


class RecipeCreate(RecipeBase):
    source: RecipeSource = RecipeSource.MANUAL
    base_prompt: Optional[str] = None
    llm_response: Optional[Dict[str, Any]] = None
    tag_ids: Optional[List[int]] = None


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None
    servings: Optional[int] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    equipment: Optional[List[str]] = None
    plating_notes: Optional[str] = None
    is_public: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class Recipe(RecipeBase):
    id: int
    user_id: int
    source: RecipeSource
    base_prompt: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    avg_rating: Optional[float] = None
    rating_count: int = 0
    tags: List["Tag"] = []
    hero_photo: Optional[str] = None

    class Config:
        from_attributes = True


# Tag schemas
class TagBase(BaseModel):
    name: str
    type: Optional[str] = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Photo schemas
class PhotoBase(BaseModel):
    recipe_id: int
    caption: Optional[str] = None
    is_hero: bool = False


class PhotoCreate(PhotoBase):
    url: str


class Photo(PhotoBase):
    id: int
    user_id: int
    url: str
    created_at: datetime

    class Config:
        from_attributes = True


# Rating schemas
class RatingBase(BaseModel):
    recipe_id: int
    score: float = Field(ge=1, le=5)
    notes: Optional[str] = None
    cooked_date: Optional[datetime] = None


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# LLM schemas
class LLMGenerateRequest(BaseModel):
    prompt: str
    style: Optional[str] = "restaurant-style"
    servings: int = 4


class LLMGenerateResponse(BaseModel):
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    equipment: Optional[List[str]] = None
    plating_notes: Optional[str] = None
    suggested_tags: Optional[List[str]] = None


# Search schemas
class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 20


class SearchResponse(BaseModel):
    internal_results: List[Recipe]
    suggest_llm: bool
    llm_result: Optional[LLMGenerateResponse] = None
