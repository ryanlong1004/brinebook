# Contributing to BrineBook

Thank you for your interest in contributing to BrineBook! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/brinebook.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with descriptive messages
7. Push to your fork
8. Create a Pull Request

## Development Setup

Follow the [Development Guide](docs/DEVELOPMENT.md) to set up your local environment.

## Code Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for complex functions
- Keep functions focused and single-purpose
- Use meaningful variable names

Example:

```python
from typing import List

def get_recipes_by_tags(
    db: Session,
    tag_ids: List[int],
    limit: int = 20
) -> List[Recipe]:
    """
    Retrieve recipes filtered by tag IDs.

    Args:
        db: Database session
        tag_ids: List of tag IDs to filter by
        limit: Maximum number of results

    Returns:
        List of Recipe objects
    """
    # Implementation
```

### JavaScript (Frontend)

- Use Vue 3 Composition API
- Prefer `const` over `let`
- Use async/await instead of promises
- Keep components small and focused
- Use TypeScript types where beneficial

Example:

```javascript
<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const loading = ref(false)

const filteredItems = computed(() => {
  return items.value.filter(item => item.active)
})

onMounted(async () => {
  await fetchItems()
})
</script>
```

## Commit Messages

Use clear, descriptive commit messages:

- `feat: Add recipe revision with AI feedback`
- `fix: Correct photo upload endpoint validation`
- `docs: Update API documentation`
- `refactor: Simplify search service logic`
- `test: Add tests for rating system`
- `chore: Update dependencies`

## Pull Request Process

1. **Update Documentation**: If adding features, update relevant docs
2. **Add Tests**: Include tests for new functionality
3. **Check Linting**: Run linters before submitting
4. **Update CHANGELOG**: Add entry describing your changes
5. **Reference Issues**: Link to related issues in PR description

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

How has this been tested?

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings
```

## Areas for Contribution

### High Priority

- Full JWT authentication system
- Recipe import from URL
- Mobile responsive improvements
- Performance optimizations
- Test coverage improvements

### Features

- Recipe collections/folders
- Shopping list generation
- Meal planning calendar
- Nutrition information
- Print-friendly views
- Recipe sharing

### Documentation

- Tutorial videos
- More API examples
- Deployment guides
- Translation to other languages

### Testing

- Unit tests for services
- Integration tests for API
- E2E tests for critical flows
- Performance benchmarks

## Reporting Bugs

Use GitHub Issues with the following information:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Numbered steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, browser, Docker version, etc.
6. **Screenshots**: If applicable
7. **Logs**: Relevant error logs

## Feature Requests

Use GitHub Issues with:

1. **Use Case**: Why this feature is needed
2. **Proposed Solution**: How it could work
3. **Alternatives**: Other approaches considered
4. **Additional Context**: Screenshots, mockups, etc.

## Code Review Process

All PRs require:

- At least one approval
- Passing CI checks
- Up-to-date with main branch
- Resolved conversations

Reviewers will check:

- Code quality and style
- Test coverage
- Documentation updates
- Performance implications
- Security considerations

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Celebrate contributions
- Follow code of conduct

## Questions?

- Open a GitHub Discussion
- Check existing documentation
- Review closed issues
- Ask in pull request comments

Thank you for contributing to BrineBook! 🍳
