# BrineBook - Complete Project Overview

## 🎯 What is BrineBook?

BrineBook is a production-ready, AI-powered recipe management application designed specifically for **restaurant-quality recipes**. It solves the problem of losing great ChatGPT-generated recipes by providing a structured vault with intelligent search, organization, and refinement capabilities.

## 🏗️ Architecture

### Technology Stack

**Backend**

- **FastAPI** (Python 3.11+) - High-performance async API framework
- **PostgreSQL** - Relational database with full-text search
- **SQLAlchemy** - ORM with Alembic migrations
- **OpenAI API** - GPT-4 for recipe generation
- **Boto3** - S3-compatible storage for photos

**Frontend**

- **Vue 3** - Progressive JavaScript framework with Composition API
- **Vite** - Next-generation frontend tooling
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Heroicons** - Beautiful hand-crafted SVG icons

**Infrastructure**

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** (production) - Reverse proxy and static file serving

## 📁 Project Structure

```
brinebook/
├── backend/                        # FastAPI Backend
│   ├── alembic/                   # Database migrations
│   │   ├── versions/
│   │   │   ├── 001_initial_migration.py
│   │   │   └── 002_seed_tags.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/                   # API route handlers
│   │   │   ├── auth.py           # User authentication
│   │   │   ├── recipes.py        # Recipe CRUD + AI generation
│   │   │   ├── search.py         # Universal search
│   │   │   ├── photos.py         # Photo management
│   │   │   ├── ratings.py        # Rating system
│   │   │   └── tags.py           # Tag management
│   │   ├── core/                 # Core configuration
│   │   │   ├── config.py         # Application settings
│   │   │   ├── database.py       # DB connection & session
│   │   │   └── security.py       # JWT & password hashing
│   │   ├── models/               # SQLAlchemy models
│   │   │   └── __init__.py       # User, Recipe, Tag, Photo, Rating
│   │   ├── schemas/              # Pydantic schemas
│   │   │   └── __init__.py       # Request/response models
│   │   ├── services/             # Business logic
│   │   │   ├── llm_service.py    # OpenAI integration
│   │   │   ├── search_service.py # Search algorithms
│   │   │   └── storage_service.py# S3 photo storage
│   │   └── main.py               # FastAPI application
│   ├── alembic.ini               # Alembic configuration
│   ├── Dockerfile                # Backend container
│   └── requirements.txt          # Python dependencies
│
├── frontend/                      # Vue 3 Frontend
│   ├── src/
│   │   ├── api/                  # API client
│   │   │   └── client.js         # Axios instance & endpoints
│   │   ├── components/           # Reusable components
│   │   │   ├── Navbar.vue        # Top navigation
│   │   │   ├── RecipeCard.vue    # Recipe grid item
│   │   │   └── SearchModal.vue   # Universal search modal
│   │   ├── stores/               # Pinia state stores
│   │   │   ├── recipes.js        # Recipe state
│   │   │   ├── search.js         # Search state
│   │   │   └── tags.js           # Tag state
│   │   ├── views/                # Page components
│   │   │   ├── Home.vue          # Recipe list/grid
│   │   │   ├── RecipeDetail.vue  # Single recipe view
│   │   │   └── NewRecipe.vue     # Create/edit form
│   │   ├── router/               # Vue Router
│   │   │   └── index.js          # Route definitions
│   │   ├── App.vue               # Root component
│   │   ├── main.js               # Application entry
│   │   └── style.css             # Global styles
│   ├── public/                   # Static assets
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── tailwind.config.js        # Tailwind configuration
│   ├── postcss.config.js         # PostCSS configuration
│   └── Dockerfile                # Frontend container
│
├── docs/                          # Documentation
│   ├── API.md                    # API reference
│   └── DEVELOPMENT.md            # Development guide
│
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker orchestration
├── setup.sh                      # Setup script
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick reference
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guidelines
└── LICENSE                       # MIT License
```

## 🔑 Key Features

### 1. AI-Powered Recipe Generation

- Structured prompts ensure consistent, restaurant-quality output
- JSON schema enforcement for reliable parsing
- Automatic tag suggestions based on content
- Equipment and plating recommendations included

### 2. Universal Search

- Searches local recipes first (fast)
- Automatically suggests AI generation for new queries
- Weighted full-text search (title > tags > ingredients > method)
- Real-time results as you type

### 3. Smart Organization

- Multi-dimensional tagging system:
  - **Cuisine**: Italian, Mexican, French, etc.
  - **Protein**: Chicken, Beef, Fish, Vegetarian, etc.
  - **Style**: Restaurant-style, Bar-food, Fine-dining, etc.
  - **Difficulty**: Easy, Intermediate, Advanced, Professional
  - **Equipment**: Sous-vide, Smoker, Cast-iron, etc.
  - **Occasion**: Weeknight, Date-night, Catering, etc.
  - **Status**: Untested, Tested, Keeper, Needs-tweak

### 4. Recipe Management

- Full CRUD operations
- Structured ingredient storage (amount, unit, notes)
- Step-by-step instructions
- Professional plating notes
- Multi-photo gallery with hero image
- Recipe revision with AI feedback

### 5. Rating System

- 5-star ratings
- Detailed notes ("Too salty", "Perfect for service")
- Cooking date tracking
- Aggregated ratings for sorting/filtering

### 6. Professional UX

- Dark mode by default (easy on the eyes)
- Keyboard shortcuts (Cmd/Ctrl+K for search)
- Command palette navigation
- Responsive design
- Fast, smooth transitions

## 🗄️ Database Schema

```sql
users
  - id, email, name, hashed_password, is_active
  - created_at, updated_at

recipes
  - id, user_id, title, description
  - source (llm|manual|web)
  - base_prompt, llm_response
  - instructions, ingredients (JSON)
  - servings, prep_time, cook_time
  - equipment (array), plating_notes
  - is_public, created_at, updated_at

tags
  - id, name, type
  - created_at

recipe_tags
  - id, recipe_id, tag_id
  - created_at

photos
  - id, recipe_id, user_id
  - url, caption, is_hero
  - created_at

ratings
  - id, recipe_id, user_id
  - score (1-5), notes, cooked_date
  - created_at
```

## 🔌 API Endpoints

### Recipes

- `POST /api/recipes/generate` - Generate with AI
- `POST /api/recipes/` - Create recipe
- `GET /api/recipes/` - List recipes
- `GET /api/recipes/{id}` - Get recipe
- `PUT /api/recipes/{id}` - Update recipe
- `DELETE /api/recipes/{id}` - Delete recipe
- `POST /api/recipes/{id}/revise` - Revise with AI

### Search

- `POST /api/search/` - Universal search

### Tags

- `GET /api/tags/` - List tags
- `POST /api/tags/` - Create tag
- `GET /api/tags/{id}` - Get tag
- `DELETE /api/tags/{id}` - Delete tag

### Photos

- `POST /api/photos/` - Upload photo
- `GET /api/photos/recipe/{id}` - Get recipe photos
- `DELETE /api/photos/{id}` - Delete photo
- `PUT /api/photos/{id}/hero` - Set hero photo

### Ratings

- `POST /api/ratings/` - Create rating
- `GET /api/ratings/recipe/{id}` - Get recipe ratings
- `PUT /api/ratings/{id}` - Update rating
- `DELETE /api/ratings/{id}` - Delete rating

## 🚀 Deployment Guide

### Local Development

```bash
# 1. Clone repository
git clone <repo-url>
cd brinebook

# 2. Setup environment
cp .env.example .env
# Add your OPENAI_API_KEY

# 3. Run setup
chmod +x setup.sh
./setup.sh

# Access at http://localhost:5173
```

### Production Deployment

**Option 1: Docker Compose (Recommended for single server)**

```bash
# 1. Setup production environment
cp .env.example .env
# Configure production values

# 2. Build and start
docker-compose -f docker-compose.prod.yml up -d

# 3. Run migrations
docker-compose exec backend alembic upgrade head
```

**Option 2: Kubernetes (Recommended for scale)**

```yaml
# Deploy to k8s cluster
kubectl apply -f k8s/
```

**Option 3: Cloud Platform (AWS/GCP/Azure)**

- Backend: AWS ECS/Fargate or Google Cloud Run
- Frontend: S3 + CloudFront or Vercel
- Database: RDS PostgreSQL or Cloud SQL
- Storage: S3 or Google Cloud Storage

## 🔐 Security Considerations

### Current Implementation

- Password hashing with bcrypt
- JWT tokens for authentication
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)
- Environment variable configuration

### Production Recommendations

1. Enable HTTPS (Let's Encrypt)
2. Rate limiting on API endpoints
3. Input validation and sanitization
4. Secure S3 bucket policies
5. Database encryption at rest
6. Regular security audits
7. API key rotation
8. User session management

## 📊 Performance Optimizations

### Backend

- Async FastAPI endpoints
- Database connection pooling
- Query optimization with indexes
- Pagination for large result sets
- Caching strategy for common queries

### Frontend

- Code splitting with dynamic imports
- Lazy loading of routes
- Image optimization
- Debounced search input
- Optimistic UI updates

### Database

- GIN indexes for full-text search
- B-tree indexes on foreign keys
- Compound indexes for common queries
- Query plan analysis

## 🧪 Testing Strategy

### Backend Tests

```python
# Unit tests
tests/unit/test_services.py
tests/unit/test_models.py

# Integration tests
tests/integration/test_api.py
tests/integration/test_database.py

# Run tests
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests

```javascript
// Unit tests
tests/unit/components/*.spec.js
tests/unit/stores/*.spec.js

// E2E tests
tests/e2e/recipe-flow.spec.js

// Run tests
npm run test
npm run test:e2e
```

## 🔄 CI/CD Pipeline

```yaml
# .github/workflows/main.yml
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    - Lint backend (flake8, mypy)
    - Lint frontend (eslint)
    - Run backend tests
    - Run frontend tests
  build:
    - Build Docker images
    - Push to registry
  deploy:
    - Deploy to staging
    - Run smoke tests
    - Deploy to production
```

## 📈 Scalability Considerations

### Horizontal Scaling

- Stateless API servers (scale with load balancer)
- Read replicas for database
- CDN for static assets
- Message queue for background jobs

### Vertical Scaling

- Increase container resources
- Database optimization
- Caching layer (Redis)

### Future Enhancements

- Elasticsearch for advanced search
- Redis for caching and sessions
- Celery for background tasks
- WebSockets for real-time features

## 💡 Development Workflow

1. **Feature Development**

   - Create feature branch
   - Implement backend changes
   - Write tests
   - Implement frontend changes
   - Update documentation
   - Submit PR

2. **Code Review**

   - Automated tests pass
   - Code review approval
   - Documentation complete
   - No merge conflicts

3. **Deployment**
   - Merge to main
   - CI/CD pipeline runs
   - Deploy to staging
   - Manual testing
   - Deploy to production

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue 3 Docs](https://vuejs.org/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [OpenAI API](https://platform.openai.com/docs/)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

See CONTRIBUTING.md for guidelines

## 📞 Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Discussions: GitHub Discussions

---

Built with ❤️ for restaurant-quality cooking at home
