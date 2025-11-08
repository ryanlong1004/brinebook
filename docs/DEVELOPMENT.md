# Development Guide

## Project Structure

```
brinebook/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # Route handlers
│   │   │   ├── auth.py     # Authentication
│   │   │   ├── recipes.py  # Recipe CRUD + AI generation
│   │   │   ├── search.py   # Universal search
│   │   │   ├── photos.py   # Photo uploads
│   │   │   ├── ratings.py  # Recipe ratings
│   │   │   └── tags.py     # Tag management
│   │   ├── core/           # Core configuration
│   │   │   ├── config.py   # Settings
│   │   │   ├── database.py # DB connection
│   │   │   └── security.py # JWT, password hashing
│   │   ├── models/         # SQLAlchemy models
│   │   │   └── __init__.py # User, Recipe, Tag, Photo, Rating
│   │   ├── schemas/        # Pydantic schemas
│   │   │   └── __init__.py # Request/response models
│   │   └── services/       # Business logic
│   │       ├── llm_service.py     # OpenAI integration
│   │       ├── search_service.py  # Search logic
│   │       └── storage_service.py # S3 uploads
│   ├── alembic/            # Database migrations
│   └── tests/
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # Vue components
│   │   │   ├── Navbar.vue
│   │   │   ├── RecipeCard.vue
│   │   │   └── SearchModal.vue
│   │   ├── stores/        # Pinia stores
│   │   │   ├── recipes.js
│   │   │   ├── search.js
│   │   │   └── tags.js
│   │   ├── views/         # Page views
│   │   │   ├── Home.vue
│   │   │   ├── RecipeDetail.vue
│   │   │   └── NewRecipe.vue
│   │   └── router/        # Vue Router
│   └── public/
└── docs/
```

## Backend Development

### Adding a New Endpoint

1. **Create route handler** in `backend/app/api/`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return {"items": []}
```

2. **Add to main.py**:

```python
from app.api import your_module
app.include_router(your_module.router, prefix="/api/items", tags=["items"])
```

### Database Migrations

Create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "Add new table"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

### LLM Integration

The `llm_service.py` uses structured prompts to ensure consistent output:

```python
from app.services.llm_service import generate_recipe

result = await generate_recipe(LLMGenerateRequest(
    prompt="restaurant style carbonara",
    style="restaurant-style",
    servings=4
))
```

Key features:

- JSON schema enforcement
- Structured ingredient parsing
- Equipment recommendations
- Plating suggestions
- Auto-tag generation

### Adding New Tag Types

1. Update `docs/API.md` with new tag type
2. Seed database with default tags
3. Update frontend tag filters

## Frontend Development

### Component Structure

**Presentational Components:**

- Pure Vue components
- Props for data
- Emit events for actions
- No direct store access

**Container Components (Views):**

- Connect to Pinia stores
- Handle business logic
- Pass data to presentational components

### Adding a New View

1. **Create view** in `src/views/`:

```vue
<template>
  <div>
    <h1>My View</h1>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
</script>
```

2. **Add route** in `src/router/index.js`:

```javascript
{
  path: '/my-view',
  name: 'my-view',
  component: () => import('../views/MyView.vue')
}
```

### State Management with Pinia

Create a new store in `src/stores/`:

```javascript
import { defineStore } from "pinia";
import { ref } from "vue";

export const useMyStore = defineStore("my-store", () => {
  const items = ref([]);
  const loading = ref(false);

  const fetchItems = async () => {
    loading.value = true;
    try {
      // API call
    } finally {
      loading.value = false;
    }
  };

  return { items, loading, fetchItems };
});
```

### Styling Guidelines

- Use Tailwind utility classes
- Follow existing color scheme (gray-900 background, primary-600 accents)
- Reuse component classes: `.btn`, `.card`, `.input`, `.badge`
- Dark mode by default

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Deployment

### Production Build

**Backend:**

```bash
cd backend
docker build -t brinebook-backend .
```

**Frontend:**

```bash
cd frontend
npm run build
```

### Environment Variables

Production `.env`:

```env
DATABASE_URL=postgresql://user:pass@prod-db:5432/brinebook
OPENAI_API_KEY=sk-prod-key
SECRET_KEY=long-random-string
S3_BUCKET_NAME=prod-brinebook-photos
ENVIRONMENT=production
```

### Database Backups

```bash
docker-compose exec db pg_dump -U brinebook brinebook > backup.sql
```

## Troubleshooting

### Common Issues

**Port already in use:**

```bash
docker-compose down
lsof -ti:5173 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Database connection failed:**

```bash
docker-compose restart db
docker-compose logs db
```

**OpenAI API errors:**

- Check API key in `.env`
- Verify account has credits
- Check rate limits

**Frontend not connecting to backend:**

- Verify `VITE_API_BASE_URL` in `.env`
- Check CORS settings in `backend/app/core/config.py`

## Code Style

**Python (Backend):**

- Follow PEP 8
- Use type hints
- Document complex functions

**JavaScript (Frontend):**

- Use Composition API
- Prefer `async/await` over promises
- Use descriptive variable names

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Create pull request
5. Wait for review
