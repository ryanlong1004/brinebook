<div align="center">
  <img src="frontend/public/images/logo-main.png" alt="BrineBook Main Logo" width="300">
</div>

<div align="center">
  <img src="frontend/public/images/logo-main.png" alt="BrineBook Main Logo" width="200">
</div>

---

## Branding & Logo

BrineBook uses a professional culinary theme with a single main logo:

- ![Main Logo](frontend/public/images/logo-main.png) (app header, navigation)

See [BRANDING.md](docs/BRANDING.md) for full guidelines, logo usage, and color palette.

---

## Developer Documentation

BrineBook is designed for easy contribution. See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for:

- Project structure and file layout
- How to add backend API endpoints (FastAPI)
- Database migrations (Alembic)
- LLM integration and prompt design
- Frontend component/view patterns (Vue 3, Pinia)
- State management, routing, and styling (Tailwind)
- Testing (pytest, npm run test)
- Deployment and environment setup
- Troubleshooting common issues
- Code style and best practices
- Contribution workflow (feature branches, PRs, review)

API details: [API.md](docs/API.md)

# BrineBook

**Your AI-powered, restaurant-style recipe vault**

BrineBook lets you generate, store, rate, tag, and rediscover restaurant-quality recipes—especially ones sourced from LLMs—without losing them in random chats.

## Features

---

## Quick Start

### Prerequisites

### Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

### Run with Docker

```bash
docker-compose up -d
```

The application will be available at:

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
brinebook/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, security, database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic, LLM integration
│   ├── alembic/         # Database migrations
│   └── tests/
├── frontend/            # Vue 3 frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── views/       # Page views
│   │   ├── stores/      # Pinia stores
│   │   ├── api/         # API client
│   │   └── router/      # Vue Router
│   └── public/
└── docker-compose.yml
```

---

## Core Workflows

### 1. Generate Recipe from AI

1. Type your query in the universal search bar: `restaurant style tuscan chicken`
2. Click "Generate with AI" if no existing recipes match
3. Review the generated recipe
4. Edit, add tags, and save

### 2. Save & Organize

### 3. Add Photos

### 4. Rate & Refine

### 5. Universal Search

- `/new "restaurant style chicken francaise"` - Generate new recipe
- `/revise <recipe>` - Send to AI for improvements
- `/menu "Italian night for 20"` - Build menu from your recipes

---

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

---

## Tech Stack

---

## License

MIT

# BrineBook

**Your AI-powered, restaurant-style recipe vault**
MIT
