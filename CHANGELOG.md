# Changelog

All notable changes to BrineBook will be documented in this file.

## [1.0.0] - 2025-11-07

### Added

- Initial release of BrineBook
- AI-powered recipe generation using OpenAI GPT-4
- Universal search combining local recipes and AI generation
- Recipe CRUD operations (Create, Read, Update, Delete)
- Multi-photo upload support with hero image selection
- 5-star rating system with notes
- Comprehensive tagging system:
  - Cuisine types (Italian, Mexican, French, etc.)
  - Protein types (Chicken, Beef, Pork, Fish, etc.)
  - Cooking styles (Restaurant-style, Elevated-diner, Bar-food)
  - Difficulty levels
  - Equipment tags (Sous-vide, Smoker, Cast-iron, etc.)
  - Occasion tags (Weeknight, Date-night, Catering, etc.)
  - Status tags (Untested, Tested, Keeper, Needs-tweak)
- Recipe revision with AI feedback integration
- Structured ingredient storage with amounts, units, and notes
- Equipment recommendations
- Professional plating notes
- Dark mode UI with Tailwind CSS
- Keyboard shortcuts (Cmd/Ctrl+K for search)
- Command palette navigation
- Docker Compose development environment
- PostgreSQL database with full-text search
- Alembic database migrations
- FastAPI backend with OpenAPI documentation
- Vue 3 frontend with Pinia state management
- S3-compatible photo storage (AWS S3 or Wasabi)

### API Features

- `/api/recipes/generate` - Generate recipes with AI
- `/api/recipes/` - Full CRUD operations
- `/api/search/` - Universal search with AI suggestions
- `/api/photos/` - Photo upload and management
- `/api/ratings/` - Recipe rating system
- `/api/tags/` - Tag management

### Frontend Features

- Recipe card grid with ratings and photos
- Detailed recipe view with ingredients and instructions
- Interactive search modal with live results
- Recipe creation/editing form
- Tag filtering and organization
- Photo gallery with hero image selection
- Rating widget with notes

### Documentation

- Comprehensive README with quick start guide
- API documentation with examples
- Development guide with best practices
- Docker setup scripts

## Future Enhancements

### Planned for v1.1

- [ ] Full JWT authentication system
- [ ] User profiles and settings
- [ ] Recipe collections/folders
- [ ] Share recipes publicly
- [ ] Recipe scaling calculator
- [ ] Shopping list generation
- [ ] Meal planning calendar
- [ ] Recipe import from URL
- [ ] Nutrition information
- [ ] Print-friendly recipe view

### Planned for v1.2

- [ ] Mobile app (iOS/Android)
- [ ] Recipe collaboration features
- [ ] Social features (following, likes, comments)
- [ ] Advanced search filters
- [ ] Recipe version history
- [ ] Cost tracking per recipe
- [ ] Inventory management
- [ ] Recipe recommendations based on available ingredients
- [ ] Multi-language support
- [ ] Voice commands for cooking mode

### Under Consideration

- Integration with smart kitchen devices
- Video tutorials integration
- Cooking timer integration
- Temperature monitoring
- Wine pairing suggestions
- Restaurant menu builder
- Catering calculator
- Batch cooking support
- Recipe analytics and insights
