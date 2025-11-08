from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Float,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RecipeSource(str, enum.Enum):
    LLM = "llm"
    MANUAL = "manual"
    WEB = "web"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    recipes = relationship("Recipe", back_populates="user")
    photos = relationship("Photo", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    source = Column(SQLEnum(RecipeSource), nullable=False, default=RecipeSource.MANUAL)
    base_prompt = Column(Text)  # Original ChatGPT prompt
    llm_response = Column(JSON)  # Raw LLM response
    instructions = Column(Text)  # Cleaned method
    ingredients = Column(
        JSON
    )  # Structured: [{"name": "chicken", "amount": "2", "unit": "lbs"}]
    servings = Column(Integer, default=4)
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    equipment = Column(ARRAY(String))  # ['sous-vide', 'cast-iron', 'smoker']
    plating_notes = Column(Text)
    hero_photo = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="recipes")
    tags = relationship(
        "RecipeTag", back_populates="recipe", cascade="all, delete-orphan"
    )
    photos = relationship(
        "Photo", back_populates="recipe", cascade="all, delete-orphan"
    )
    ratings = relationship(
        "Rating", back_populates="recipe", cascade="all, delete-orphan"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    type = Column(
        String, index=True
    )  # cuisine, protein, style, difficulty, equipment, occasion, status
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipes = relationship("RecipeTag", back_populates="tag")


class RecipeTag(Base):
    __tablename__ = "recipe_tags"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipe = relationship("Recipe", back_populates="tags")
    tag = relationship("Tag", back_populates="recipes")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    caption = Column(Text)
    is_hero = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipe = relationship("Recipe", back_populates="photos")
    user = relationship("User", back_populates="photos")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)  # 1-5 stars
    notes = Column(Text)
    cooked_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipe = relationship("Recipe", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
