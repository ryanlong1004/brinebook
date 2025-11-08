"""Seed initial tags

Revision ID: 002
Revises: 001
Create Date: 2025-11-07

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Seed default tags
    op.execute("""
        INSERT INTO tags (name, type) VALUES
        -- Cuisine
        ('italian', 'cuisine'),
        ('mexican', 'cuisine'),
        ('french', 'cuisine'),
        ('chinese', 'cuisine'),
        ('japanese', 'cuisine'),
        ('thai', 'cuisine'),
        ('indian', 'cuisine'),
        ('american', 'cuisine'),
        ('mediterranean', 'cuisine'),
        ('korean', 'cuisine'),
        
        -- Protein
        ('chicken', 'protein'),
        ('beef', 'protein'),
        ('pork', 'protein'),
        ('fish', 'protein'),
        ('seafood', 'protein'),
        ('lamb', 'protein'),
        ('vegetarian', 'protein'),
        ('vegan', 'protein'),
        
        -- Style
        ('restaurant-style', 'style'),
        ('elevated-diner', 'style'),
        ('bar-food', 'style'),
        ('street-food', 'style'),
        ('fine-dining', 'style'),
        ('comfort-food', 'style'),
        ('fusion', 'style'),
        
        -- Difficulty
        ('easy', 'difficulty'),
        ('intermediate', 'difficulty'),
        ('advanced', 'difficulty'),
        ('professional', 'difficulty'),
        
        -- Equipment
        ('sous-vide', 'equipment'),
        ('smoker', 'equipment'),
        ('cast-iron', 'equipment'),
        ('flat-top', 'equipment'),
        ('grill', 'equipment'),
        ('pressure-cooker', 'equipment'),
        ('air-fryer', 'equipment'),
        ('dutch-oven', 'equipment'),
        
        -- Occasion
        ('weeknight', 'occasion'),
        ('date-night', 'occasion'),
        ('brunch', 'occasion'),
        ('menu-special', 'occasion'),
        ('catering', 'occasion'),
        ('batch-cooking', 'occasion'),
        ('meal-prep', 'occasion'),
        ('entertaining', 'occasion'),
        
        -- Status
        ('untested', 'status'),
        ('tested', 'status'),
        ('keeper', 'status'),
        ('needs-tweak', 'status')
    """)


def downgrade() -> None:
    # Delete seeded tags
    op.execute(
        "DELETE FROM tags WHERE type IN ('cuisine', 'protein', 'style', 'difficulty', 'equipment', 'occasion', 'status')"
    )
