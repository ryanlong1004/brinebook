"""Add hero_photo column to recipes

Revision ID: 004
Revises: 003
Create Date: 2025-11-07
"""

from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("recipes", sa.Column("hero_photo", sa.String(), nullable=True))

    # Set hero_photo for recipes 1-10
    demo_images = [
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        "https://images.unsplash.com/photo-1519864600265-abb23847ef2c",
        "https://images.unsplash.com/photo-1464306076886-debede6bbf09",
        "https://images.unsplash.com/photo-1502741338009-cac2772e18bc",
        "https://images.unsplash.com/photo-1523987355523-c7b5b0723c6b",
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        "https://images.unsplash.com/photo-1519864600265-abb23847ef2c",
        "https://images.unsplash.com/photo-1464306076886-debede6bbf09",
        "https://images.unsplash.com/photo-1502741338009-cac2772e18bc",
        "https://images.unsplash.com/photo-1523987355523-c7b5b0723c6b",
    ]
    for i, url in enumerate(demo_images, start=1):
        op.execute(f"UPDATE recipes SET hero_photo = '{url}' WHERE id = {i}")


def downgrade() -> None:
    op.drop_column("recipes", "hero_photo")
