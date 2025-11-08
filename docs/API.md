# BrineBook API Documentation

## Authentication

Currently using a simplified auth system. Full JWT implementation coming soon.

## Endpoints

### Recipes

#### Generate Recipe with AI

```http
POST /api/recipes/generate
Content-Type: application/json

{
  "prompt": "restaurant style tuscan chicken",
  "style": "restaurant-style",
  "servings": 4
}
```

**Response:**

```json
{
  "title": "Restaurant-Style Tuscan Chicken",
  "description": "Pan-seared chicken in a creamy sun-dried tomato sauce...",
  "ingredients": [
    {
      "name": "chicken breast",
      "amount": "4",
      "unit": "pieces",
      "notes": "pounded to even thickness"
    }
  ],
  "instructions": "1. Season chicken...\n2. Heat pan...",
  "prep_time": 15,
  "cook_time": 25,
  "equipment": ["cast-iron skillet", "meat thermometer"],
  "plating_notes": "Serve over creamy polenta...",
  "suggested_tags": ["italian", "chicken", "date-night"]
}
```

#### Create Recipe

```http
POST /api/recipes/
Content-Type: application/json

{
  "title": "Restaurant-Style Tuscan Chicken",
  "description": "Brief description",
  "source": "llm",
  "base_prompt": "restaurant style tuscan chicken",
  "instructions": "Step by step...",
  "ingredients": [...],
  "servings": 4,
  "tag_ids": [1, 2, 3]
}
```

#### List Recipes

```http
GET /api/recipes/?skip=0&limit=20&source=llm&tag_ids=1,2
```

#### Get Recipe

```http
GET /api/recipes/{id}
```

#### Update Recipe

```http
PUT /api/recipes/{id}
Content-Type: application/json

{
  "title": "Updated Title",
  "servings": 6
}
```

#### Delete Recipe

```http
DELETE /api/recipes/{id}
```

#### Revise Recipe with AI

```http
POST /api/recipes/{id}/revise
Content-Type: application/json

{
  "notes": "Too salty, needs more acidity"
}
```

### Search

#### Universal Search

```http
POST /api/search/
Content-Type: application/json

{
  "query": "tuscan chicken",
  "filters": {
    "tags": [1, 2],
    "min_rating": 4.0
  },
  "limit": 20
}
```

**Response:**

```json
{
  "internal_results": [...],
  "suggest_llm": true,
  "llm_result": {...}
}
```

### Tags

#### List Tags

```http
GET /api/tags/?type=cuisine
```

#### Create Tag

```http
POST /api/tags/
Content-Type: application/json

{
  "name": "italian",
  "type": "cuisine"
}
```

### Photos

#### Upload Photo

```http
POST /api/photos/
Content-Type: multipart/form-data

recipe_id=1
file=<binary>
caption="Plated dish"
is_hero=true
```

#### Get Recipe Photos

```http
GET /api/photos/recipe/{recipe_id}
```

#### Delete Photo

```http
DELETE /api/photos/{photo_id}
```

#### Set Hero Photo

```http
PUT /api/photos/{photo_id}/hero
```

### Ratings

#### Create Rating

```http
POST /api/ratings/
Content-Type: application/json

{
  "recipe_id": 1,
  "score": 4.5,
  "notes": "Perfect for service",
  "cooked_date": "2025-11-07T12:00:00Z"
}
```

#### Get Recipe Ratings

```http
GET /api/ratings/recipe/{recipe_id}
```

## Data Models

### Recipe

```typescript
{
  id: number
  user_id: number
  title: string
  description?: string
  source: "llm" | "manual" | "web"
  base_prompt?: string
  instructions?: string
  ingredients: Ingredient[]
  servings: number
  prep_time?: number
  cook_time?: number
  equipment?: string[]
  plating_notes?: string
  is_public: boolean
  created_at: datetime
  updated_at?: datetime
  avg_rating?: number
  rating_count: number
  tags: Tag[]
  hero_photo?: string
}
```

### Ingredient

```typescript
{
  name: string
  amount: string
  unit?: string
  notes?: string
}
```

### Tag Types

- `cuisine`: italian, mexican, french, etc.
- `protein`: chicken, beef, pork, fish, etc.
- `style`: restaurant-style, elevated-diner, bar-food, etc.
- `difficulty`: easy, intermediate, advanced, professional
- `equipment`: sous-vide, smoker, flat-top, cast-iron, etc.
- `occasion`: weeknight, date-night, menu-special, catering, brunch
- `status`: untested, tested, keeper, needs-tweak

## Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

Error response format:

```json
{
  "detail": "Error message"
}
```
