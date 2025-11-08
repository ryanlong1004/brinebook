"""Seed popular recipes

Revision ID: 003
Revises: 002
Create Date: 2025-11-07

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Text, JSON, Boolean

# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Set hero_photo field for each recipe (after demo_images is defined)
    for i, url in enumerate(demo_images, start=1):
        op.execute(f"UPDATE recipes SET hero_photo = '{url}' WHERE id = {i}")
    # Recipes data (using existing user_id=1)
    recipes_table = table(
        "recipes",
        column("id", Integer),
        column("user_id", Integer),
        column("title", String),
        column("description", Text),
        column("source", String),
        column("instructions", Text),
        column("ingredients", JSON),
        column("servings", Integer),
        column("prep_time", Integer),
        column("cook_time", Integer),
        column("equipment", sa.ARRAY(String)),
        column("plating_notes", Text),
        column("is_public", Boolean),
    )

    recipes = [
        {
            "id": 1,
            "user_id": 1,
            "title": "Pan-Seared Ribeye with Garlic Herb Butter",
            "description": "A perfectly seared ribeye steak with a rich garlic herb butter, cooked to perfection.",
            "source": "MANUAL",
            "instructions": """1. Remove steak from refrigerator 30 minutes before cooking
2. Pat dry and season generously with salt and pepper
3. Heat cast iron skillet over high heat until smoking
4. Sear steak 4-5 minutes per side for medium-rare
5. Add butter, garlic, and herbs to pan in last minute
6. Baste steak with melted butter
7. Rest 5 minutes before serving""",
            "ingredients": [
                {"name": "ribeye steak", "amount": "16", "unit": "oz"},
                {"name": "kosher salt", "amount": "2", "unit": "tsp"},
                {"name": "black pepper", "amount": "1", "unit": "tsp"},
                {"name": "butter", "amount": "4", "unit": "tbsp"},
                {"name": "garlic cloves", "amount": "4", "unit": "whole"},
                {"name": "fresh thyme", "amount": "3", "unit": "sprigs"},
                {"name": "fresh rosemary", "amount": "2", "unit": "sprigs"},
            ],
            "servings": 2,
            "prep_time": 35,
            "cook_time": 15,
            "equipment": ["cast-iron skillet", "tongs"],
            "plating_notes": "Slice against the grain and fan out on plate. Drizzle with herb butter.",
            "is_public": True,
        },
        {
            "id": 2,
            "user_id": 1,
            "title": "Crispy Skin Salmon with Lemon Beurre Blanc",
            "description": "Restaurant-quality salmon with perfectly crispy skin and a silky lemon butter sauce.",
            "source": "MANUAL",
            "instructions": """1. Pat salmon dry and score the skin
2. Season with salt and pepper
3. Heat oil in non-stick pan over medium-high heat
4. Place salmon skin-side down, press gently for 30 seconds
5. Cook 5-6 minutes until skin is crispy
6. Flip and cook 2 minutes more
7. Make beurre blanc: reduce wine and shallots, whisk in cold butter
8. Finish with lemon juice""",
            "ingredients": [
                {"name": "salmon fillets", "amount": "4", "unit": "6oz pieces"},
                {"name": "olive oil", "amount": "2", "unit": "tbsp"},
                {"name": "white wine", "amount": "1/2", "unit": "cup"},
                {"name": "shallot", "amount": "1", "unit": "minced"},
                {"name": "cold butter", "amount": "8", "unit": "tbsp"},
                {"name": "lemon", "amount": "1", "unit": "whole"},
                {"name": "salt", "amount": "to taste", "unit": ""},
            ],
            "servings": 4,
            "prep_time": 10,
            "cook_time": 15,
            "equipment": ["non-stick pan", "small saucepan", "whisk"],
            "plating_notes": "Place salmon skin-side up. Pool sauce underneath, garnish with microgreens.",
            "is_public": True,
        },
        {
            "id": 3,
            "user_id": 1,
            "title": "Truffle Risotto with Parmigiano-Reggiano",
            "description": "Luxuriously creamy risotto infused with truffle oil and finished with aged parmesan.",
            "source": "MANUAL",
            "instructions": """1. Heat stock in a pot and keep warm
2. Sauté shallots in butter until translucent
3. Add rice, toast for 2 minutes
4. Add wine, stir until absorbed
5. Add stock one ladle at a time, stirring constantly
6. Continue for 18-20 minutes until rice is al dente
7. Remove from heat, stir in butter, parmesan, and truffle oil
8. Let rest 2 minutes before serving""",
            "ingredients": [
                {"name": "arborio rice", "amount": "2", "unit": "cups"},
                {"name": "chicken stock", "amount": "6", "unit": "cups"},
                {"name": "white wine", "amount": "1", "unit": "cup"},
                {"name": "shallots", "amount": "2", "unit": "minced"},
                {"name": "butter", "amount": "6", "unit": "tbsp"},
                {"name": "parmigiano-reggiano", "amount": "1", "unit": "cup grated"},
                {"name": "truffle oil", "amount": "2", "unit": "tbsp"},
            ],
            "servings": 4,
            "prep_time": 10,
            "cook_time": 30,
            "equipment": ["large sauté pan", "ladle", "wooden spoon"],
            "plating_notes": "Serve in shallow bowls, shave fresh parmesan on top, drizzle with truffle oil.",
            "is_public": True,
        },
        {
            "id": 4,
            "user_id": 1,
            "title": "Sous Vide Duck Breast with Cherry Gastrique",
            "description": "Perfectly cooked duck breast with crispy skin and a sweet-tart cherry reduction.",
            "source": "MANUAL",
            "instructions": """1. Season duck breasts with salt and pepper
2. Vacuum seal and sous vide at 135°F for 2 hours
3. Remove from bag, pat dry
4. Score skin in crosshatch pattern
5. Sear skin-side down in cold pan, render fat for 8-10 minutes
6. Flip and sear 1 minute
7. Make gastrique: caramelize sugar, add vinegar and cherries
8. Reduce until syrupy""",
            "ingredients": [
                {"name": "duck breasts", "amount": "2", "unit": "whole"},
                {"name": "fresh cherries", "amount": "1", "unit": "cup pitted"},
                {"name": "sugar", "amount": "1/4", "unit": "cup"},
                {"name": "red wine vinegar", "amount": "1/4", "unit": "cup"},
                {"name": "salt", "amount": "to taste", "unit": ""},
                {"name": "black pepper", "amount": "to taste", "unit": ""},
            ],
            "servings": 2,
            "prep_time": 15,
            "cook_time": 130,
            "equipment": ["sous vide", "vacuum sealer", "cast-iron skillet"],
            "plating_notes": "Slice breast on bias, fan on plate. Drizzle gastrique around and over.",
            "is_public": True,
        },
        {
            "id": 5,
            "user_id": 1,
            "title": "Handmade Tagliatelle with Bolognese Ragu",
            "description": "Fresh pasta with a slow-cooked, rich meat sauce in the traditional Bolognese style.",
            "source": "MANUAL",
            "instructions": """1. Make pasta dough: mix flour and eggs, knead 10 minutes, rest 30 minutes
2. Roll out thin and cut into tagliatelle
3. For ragu: sauté soffritto (onion, carrot, celery) in olive oil
4. Brown ground beef and pork
5. Add tomato paste, wine, milk, and stock
6. Simmer 3-4 hours, stirring occasionally
7. Cook pasta in salted boiling water 2-3 minutes
8. Toss pasta with sauce, finish with parmesan""",
            "ingredients": [
                {"name": "00 flour", "amount": "2", "unit": "cups"},
                {"name": "eggs", "amount": "3", "unit": "large"},
                {"name": "ground beef", "amount": "1", "unit": "lb"},
                {"name": "ground pork", "amount": "1/2", "unit": "lb"},
                {"name": "onion", "amount": "1", "unit": "diced"},
                {"name": "carrot", "amount": "1", "unit": "diced"},
                {"name": "celery", "amount": "1", "unit": "stalk diced"},
                {"name": "tomato paste", "amount": "3", "unit": "tbsp"},
                {"name": "red wine", "amount": "1", "unit": "cup"},
                {"name": "whole milk", "amount": "1", "unit": "cup"},
                {"name": "beef stock", "amount": "2", "unit": "cups"},
            ],
            "servings": 6,
            "prep_time": 60,
            "cook_time": 240,
            "equipment": ["pasta machine", "large dutch oven", "pasta pot"],
            "plating_notes": "Twirl pasta into nest, top with ragu and fresh parmesan.",
            "is_public": True,
        },
        {
            "id": 6,
            "user_id": 1,
            "title": "Miso-Glazed Black Cod",
            "description": "Buttery black cod marinated in sweet miso glaze, inspired by Nobu's signature dish.",
            "source": "MANUAL",
            "instructions": """1. Mix miso, mirin, sake, and sugar for marinade
2. Marinate cod for 24-48 hours in refrigerator
3. Preheat broiler
4. Remove excess marinade from fish
5. Broil 8-10 minutes until caramelized and flaky
6. Garnish with sesame seeds and scallions""",
            "ingredients": [
                {"name": "black cod fillets", "amount": "4", "unit": "6oz pieces"},
                {"name": "white miso paste", "amount": "1/2", "unit": "cup"},
                {"name": "mirin", "amount": "1/4", "unit": "cup"},
                {"name": "sake", "amount": "1/4", "unit": "cup"},
                {"name": "sugar", "amount": "3", "unit": "tbsp"},
                {"name": "sesame seeds", "amount": "1", "unit": "tbsp"},
                {"name": "scallions", "amount": "2", "unit": "sliced"},
            ],
            "servings": 4,
            "prep_time": 1450,
            "cook_time": 10,
            "equipment": ["baking sheet", "broiler"],
            "plating_notes": "Center cod on plate, garnish with sesame and scallions. Serve with steamed rice.",
            "is_public": True,
        },
        {
            "id": 7,
            "user_id": 1,
            "title": "Beef Wellington with Red Wine Jus",
            "description": "Classic showstopper: tender beef tenderloin wrapped in mushroom duxelles and puff pastry.",
            "source": "MANUAL",
            "instructions": """1. Sear beef tenderloin on all sides, cool completely
2. Make duxelles: sauté mushrooms, shallots, thyme until dry
3. Brush beef with mustard, wrap in prosciutto
4. Roll out puff pastry, spread duxelles
5. Wrap beef tightly in pastry, egg wash
6. Refrigerate 30 minutes
7. Bake at 425°F for 25-30 minutes (medium-rare)
8. Make jus: reduce red wine with stock and shallots
9. Rest 10 minutes before slicing""",
            "ingredients": [
                {"name": "beef tenderloin", "amount": "2", "unit": "lb center cut"},
                {"name": "puff pastry", "amount": "1", "unit": "lb"},
                {"name": "mushrooms", "amount": "1", "unit": "lb minced"},
                {"name": "prosciutto", "amount": "8", "unit": "slices"},
                {"name": "dijon mustard", "amount": "2", "unit": "tbsp"},
                {"name": "egg", "amount": "1", "unit": "beaten"},
                {"name": "red wine", "amount": "2", "unit": "cups"},
                {"name": "beef stock", "amount": "2", "unit": "cups"},
            ],
            "servings": 6,
            "prep_time": 60,
            "cook_time": 40,
            "equipment": ["cast-iron skillet", "baking sheet", "meat thermometer"],
            "plating_notes": "Slice thick, serve with jus pooled around. Garnish with fresh thyme.",
            "is_public": True,
        },
        {
            "id": 8,
            "user_id": 1,
            "title": "Lobster Thermidor",
            "description": "Decadent French classic with lobster in a creamy cognac sauce, broiled to perfection.",
            "source": "MANUAL",
            "instructions": """1. Steam lobsters 8-10 minutes, cool and split
2. Remove meat, reserve shells
3. Make sauce: sauté shallots, add cognac and flambé
4. Add cream, mustard, and seasonings
5. Fold in lobster meat
6. Fill shells with mixture
7. Top with gruyere and breadcrumbs
8. Broil until golden and bubbling""",
            "ingredients": [
                {"name": "live lobsters", "amount": "2", "unit": "1.5lb each"},
                {"name": "heavy cream", "amount": "1", "unit": "cup"},
                {"name": "cognac", "amount": "1/4", "unit": "cup"},
                {"name": "dijon mustard", "amount": "1", "unit": "tbsp"},
                {"name": "gruyere cheese", "amount": "1/2", "unit": "cup grated"},
                {"name": "panko breadcrumbs", "amount": "1/4", "unit": "cup"},
                {"name": "shallots", "amount": "2", "unit": "minced"},
                {"name": "butter", "amount": "3", "unit": "tbsp"},
            ],
            "servings": 2,
            "prep_time": 30,
            "cook_time": 20,
            "equipment": ["large pot", "broiler", "saucepan"],
            "plating_notes": "Present whole lobster on platter with lemon wedges and parsley.",
            "is_public": True,
        },
        {
            "id": 9,
            "user_id": 1,
            "title": "Coq au Vin",
            "description": "French braised chicken in red wine with pearl onions, mushrooms, and bacon.",
            "source": "MANUAL",
            "instructions": """1. Marinate chicken in wine overnight
2. Render bacon, brown chicken pieces
3. Sauté pearl onions and mushrooms
4. Add garlic, tomato paste, herbs
5. Pour in wine marinade and stock
6. Braise covered at 325°F for 1.5 hours
7. Remove chicken, reduce sauce
8. Return chicken to sauce, garnish with bacon and herbs""",
            "ingredients": [
                {"name": "chicken thighs", "amount": "8", "unit": "bone-in"},
                {"name": "red wine", "amount": "3", "unit": "cups burgundy"},
                {"name": "bacon", "amount": "6", "unit": "strips diced"},
                {"name": "pearl onions", "amount": "12", "unit": "peeled"},
                {"name": "mushrooms", "amount": "8", "unit": "oz halved"},
                {"name": "chicken stock", "amount": "2", "unit": "cups"},
                {"name": "tomato paste", "amount": "2", "unit": "tbsp"},
                {"name": "thyme", "amount": "4", "unit": "sprigs"},
                {"name": "bay leaves", "amount": "2", "unit": "whole"},
            ],
            "servings": 4,
            "prep_time": 1460,
            "cook_time": 120,
            "equipment": ["dutch oven", "large skillet"],
            "plating_notes": "Serve in shallow bowls with crusty bread for sauce.",
            "is_public": True,
        },
        {
            "id": 10,
            "user_id": 1,
            "title": "Chocolate Soufflé with Crème Anglaise",
            "description": "Light and airy chocolate soufflé with a molten center, served with vanilla custard sauce.",
            "source": "MANUAL",
            "instructions": """1. Butter and sugar ramekins
2. Make crème anglaise: temper egg yolks with hot cream and vanilla
3. Melt chocolate with butter
4. Beat egg whites to stiff peaks with sugar
5. Fold chocolate into a portion of whites, then fold in remaining whites
6. Fill ramekins 3/4 full
7. Bake at 375°F for 12-14 minutes until risen
8. Dust with powdered sugar, serve immediately with sauce""",
            "ingredients": [
                {"name": "dark chocolate", "amount": "6", "unit": "oz 70%"},
                {"name": "eggs", "amount": "4", "unit": "separated"},
                {"name": "sugar", "amount": "1/3", "unit": "cup plus extra"},
                {"name": "butter", "amount": "2", "unit": "tbsp plus extra"},
                {"name": "heavy cream", "amount": "2", "unit": "cups"},
                {"name": "vanilla bean", "amount": "1", "unit": "split"},
                {"name": "egg yolks", "amount": "6", "unit": "for sauce"},
            ],
            "servings": 4,
            "prep_time": 30,
            "cook_time": 14,
            "equipment": ["ramekins", "double boiler", "electric mixer"],
            "plating_notes": "Serve immediately in ramekins with sauce poured tableside.",
            "is_public": True,
        },
    ]

    # Insert recipes
    for recipe in recipes:
        op.execute(recipes_table.insert().values(**recipe))

    # Insert recipe tags
    recipe_tags_table = table(
        "recipe_tags",
        column("recipe_id", Integer),
        column("tag_id", Integer),
    )

    # Tag mappings (based on existing tags from 002_seed_tags.py)
    tag_mappings = [
        # Recipe 1: Ribeye - protein: beef, difficulty: intermediate
        {"recipe_id": 1, "tag_id": 2},  # beef
        {"recipe_id": 1, "tag_id": 25},  # intermediate
        # Recipe 2: Salmon - protein: fish, difficulty: intermediate
        {"recipe_id": 2, "tag_id": 4},  # fish
        {"recipe_id": 2, "tag_id": 25},  # intermediate
        # Recipe 3: Risotto - cuisine: italian, difficulty: advanced
        {"recipe_id": 3, "tag_id": 7},  # italian
        {"recipe_id": 3, "tag_id": 26},  # advanced
        # Recipe 4: Duck - protein: poultry, equipment: sous-vide, difficulty: advanced
        {"recipe_id": 4, "tag_id": 3},  # poultry
        {"recipe_id": 4, "tag_id": 18},  # sous-vide
        {"recipe_id": 4, "tag_id": 26},  # advanced
        # Recipe 5: Pasta - cuisine: italian, difficulty: advanced
        {"recipe_id": 5, "tag_id": 7},  # italian
        {"recipe_id": 5, "tag_id": 26},  # advanced
        # Recipe 6: Black Cod - cuisine: japanese, protein: fish, difficulty: intermediate
        {"recipe_id": 6, "tag_id": 9},  # japanese
        {"recipe_id": 6, "tag_id": 4},  # fish
        {"recipe_id": 6, "tag_id": 25},  # intermediate
        # Recipe 7: Beef Wellington - protein: beef, difficulty: advanced
        {"recipe_id": 7, "tag_id": 2},  # beef
        {"recipe_id": 7, "tag_id": 26},  # advanced
        # Recipe 8: Lobster - protein: shellfish, cuisine: french, difficulty: advanced
        {"recipe_id": 8, "tag_id": 5},  # shellfish
        {"recipe_id": 8, "tag_id": 6},  # french
        {"recipe_id": 8, "tag_id": 26},  # advanced
        # Recipe 9: Coq au Vin - protein: poultry, cuisine: french, difficulty: intermediate
        {"recipe_id": 9, "tag_id": 3},  # poultry
        {"recipe_id": 9, "tag_id": 6},  # french
        {"recipe_id": 9, "tag_id": 25},  # intermediate
        # Recipe 10: Soufflé - cuisine: french, difficulty: advanced
        {"recipe_id": 10, "tag_id": 6},  # french
        {"recipe_id": 10, "tag_id": 26},  # advanced
    ]

    for mapping in tag_mappings:
        op.execute(recipe_tags_table.insert().values(**mapping))

        # Seed demo hero images for each recipe
        photos_table = table(
            "photos",
            column("id", Integer),
            column("recipe_id", Integer),
            column("user_id", Integer),
            column("url", String),
            column("caption", Text),
            column("is_hero", Boolean),
        )

        demo_images = [
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836",  # Ribeye
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c",  # Salmon
            "https://images.unsplash.com/photo-1464306076886-debede6bbf09",  # Risotto
            "https://images.unsplash.com/photo-1502741338009-cac2772e18bc",  # Duck
            "https://images.unsplash.com/photo-1523987355523-c7b5b0723c6b",  # Tagliatelle
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836",  # Black Cod
            "https://images.unsplash.com/photo-1519864600265-abb23847ef2c",  # Wellington
            "https://images.unsplash.com/photo-1464306076886-debede6bbf09",  # Lobster
            "https://images.unsplash.com/photo-1502741338009-cac2772e18bc",  # Coq au Vin
            "https://images.unsplash.com/photo-1523987355523-c7b5b0723c6b",  # Soufflé
        ]
        for i, url in enumerate(demo_images, start=1):
            op.execute(
                photos_table.insert().values(
                    id=i,
                    recipe_id=i,
                    user_id=1,
                    url=url,
                    caption=f"Demo image for recipe {i}",
                    is_hero=True,
                )
            )


def downgrade() -> None:
    # Delete in reverse order due to foreign keys
    op.execute("DELETE FROM recipe_tags WHERE recipe_id BETWEEN 1 AND 10")
    op.execute("DELETE FROM recipes WHERE id BETWEEN 1 AND 10")
