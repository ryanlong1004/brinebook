# BrineBook - Quick Reference

## Commands

### Start Application

```bash
./setup.sh          # First time setup
docker-compose up   # Start all services
```

### Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Database
alembic upgrade head              # Run migrations
alembic revision --autogenerate   # Create migration
```

### Docker

```bash
docker-compose up -d              # Start in background
docker-compose down               # Stop all services
docker-compose logs -f backend    # View backend logs
docker-compose logs -f frontend   # View frontend logs
docker-compose restart backend    # Restart service
docker-compose exec db psql -U brinebook  # Access database
```

## URLs

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

## Keyboard Shortcuts

- `Cmd/Ctrl + K` - Open search modal
- `Escape` - Close modal
- `Enter` in search - Navigate to first result or generate

## Project Structure

```
brinebook/
├── backend/          # FastAPI + Python
├── frontend/         # Vue 3 + Vite
├── docs/            # Documentation
├── .env             # Environment variables
└── docker-compose.yml
```

## Environment Variables

Essential `.env` variables:

```env
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://brinebook:brinebook@db:5432/brinebook
SECRET_KEY=your-secret-key
```

## Common Tasks

### Create Recipe with AI

1. Press `Cmd/Ctrl + K`
2. Type: "restaurant style tuscan chicken"
3. Click "Generate with AI"
4. Review and save

### Add Tags to Recipe

1. Open recipe
2. Click "Edit"
3. Select tags from predefined list
4. Save

### Upload Photos

1. Open recipe detail
2. Click "Upload Photo"
3. Select file
4. Optionally set as hero image

### Rate Recipe

1. Open recipe detail
2. Click stars (1-5)
3. Add notes (optional)
4. Submit

## API Quick Examples

### Generate Recipe

```bash
curl -X POST http://localhost:8000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "restaurant style carbonara", "servings": 4}'
```

### Search Recipes

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "chicken"}'
```

### Create Recipe

```bash
curl -X POST http://localhost:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Recipe",
    "servings": 4,
    "source": "manual",
    "ingredients": [
      {"name": "salt", "amount": "1", "unit": "tsp"}
    ]
  }'
```

## Troubleshooting

### Database Issues

```bash
docker-compose restart db
docker-compose exec db psql -U brinebook -c "SELECT version();"
```

### Backend Won't Start

```bash
docker-compose logs backend
# Check for missing dependencies or configuration errors
```

### Frontend 404 Errors

```bash
# Check API connection
curl http://localhost:8000/health
# Verify VITE_API_BASE_URL in .env
```

### OpenAI Errors

- Verify API key is set
- Check account credits
- Review rate limits

## Tag Types Reference

- **cuisine**: italian, mexican, french, chinese, japanese, thai, indian
- **protein**: chicken, beef, pork, fish, seafood, lamb, vegetarian, vegan
- **style**: restaurant-style, elevated-diner, bar-food, street-food, fine-dining
- **difficulty**: easy, intermediate, advanced, professional
- **equipment**: sous-vide, smoker, cast-iron, flat-top, grill, pressure-cooker
- **occasion**: weeknight, date-night, brunch, menu-special, catering, batch-cooking
- **status**: untested, tested, keeper, needs-tweak

## Support

For issues or questions:

1. Check the documentation in `/docs`
2. Review error logs: `docker-compose logs -f`
3. Verify environment variables in `.env`
4. Check database connection
5. Ensure OpenAI API key is valid
