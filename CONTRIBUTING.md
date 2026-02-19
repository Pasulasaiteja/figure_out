# Contributing to Transformers

Thank you for considering contributing to Transformers! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

Before creating a bug report, please:
1. Check existing issues to avoid duplicates
2. Use a clear and descriptive title
3. Include steps to reproduce the bug
4. Provide error messages and screenshots
5. Specify your environment (OS, browser, versions)

**Bug Report Template:**
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Python: [e.g., 3.11]
- Node: [e.g., 18.17]

**Screenshots:**
If applicable
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Use a clear and descriptive title
2. Provide a detailed description
3. Explain why this enhancement would be useful
4. Include mockups or examples if possible

### Pull Requests

#### Before Submitting

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/transformers.git
cd transformers
```

2. **Create a feature branch**
```bash
git checkout -b feature/AmazingFeature
```

3. **Make your changes**
- Follow the coding standards (see below)
- Test your changes thoroughly
- Update documentation if needed

4. **Commit your changes**
```bash
git add .
git commit -m "Add some AmazingFeature"
```

5. **Push to your fork**
```bash
git push origin feature/AmazingFeature
```

6. **Open a Pull Request**
- Use a clear title
- Describe what you changed and why
- Reference any related issues

#### Pull Request Guidelines

- Follow existing code style
- Include tests for new features
- Update documentation
- Keep PRs focused (one feature/fix per PR)
- Ensure all tests pass
- Respond to review feedback

## Development Setup

### Backend Development

1. **Setup environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run tests**
```bash
pytest tests/
```

3. **Run server**
```bash
uvicorn main:app --reload
```

### Frontend Development

1. **Setup environment**
```bash
cd frontend
npm install
```

2. **Run tests**
```bash
npm run test
```

3. **Run dev server**
```bash
npm run dev
```

## Coding Standards

### Python (Backend)

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def calculate_calories(weight: float, duration: int) -> float:
    """Calculate calories burned during exercise.
    
    Args:
        weight: User weight in kg
        duration: Duration in minutes
        
    Returns:
        Calories burned
    """
    return weight * duration * 0.5

# Bad
def calc_cal(w,d):
    return w*d*0.5
```

**Key Points:**
- Use meaningful variable names
- Add type hints
- Write docstrings for functions/classes
- Keep functions small and focused
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)

### JavaScript/React (Frontend)

Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript):

```javascript
// Good
const WorkoutCard = ({ exercise, onComplete }) => {
  const handleComplete = () => {
    onComplete(exercise.id);
  };

  return (
    <div className="workout-card">
      <h3>{exercise.name}</h3>
      <button onClick={handleComplete}>Complete</button>
    </div>
  );
};

// Bad
const wc = (props) => {
  return <div>{props.e.name}<button onClick={() => props.oc(props.e.id)}>Complete</button></div>
}
```

**Key Points:**
- Use functional components with hooks
- Use meaningful component names (PascalCase)
- Use camelCase for variables/functions
- Destructure props
- Keep components small and reusable
- Use Tailwind CSS classes

## Project Structure

### Backend
```
backend/
├── app/
│   ├── api/          # API route handlers
│   ├── core/         # Configuration, security
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── tests/            # Test files
└── main.py           # App entry point
```

### Frontend
```
frontend/
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── services/     # API calls
│   ├── store/        # Zustand state
│   └── utils/        # Utility functions
```

## Writing Tests

### Backend Tests (pytest)

```python
# tests/test_workout.py
import pytest
from app.services.ai_service import AIService

def test_generate_workout_plan():
    ai_service = AIService()
    plan = ai_service.generate_workout_plan(
        fitness_level="Beginner",
        goals="Lose weight",
        preference="Home"
    )
    assert plan is not None
    assert len(plan["exercises"]) > 0
```

### Frontend Tests (Vitest)

```javascript
// src/components/__tests__/WorkoutCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import WorkoutCard from '../WorkoutCard';

test('calls onComplete when button clicked', () => {
  const mockComplete = jest.fn();
  render(<WorkoutCard exercise={{ name: 'Push-ups' }} onComplete={mockComplete} />);
  
  fireEvent.click(screen.getByText('Complete'));
  expect(mockComplete).toHaveBeenCalled();
});
```

## Documentation

When adding new features:

1. **Update API Documentation**
   - Add endpoint to [API_REFERENCE.md](API_REFERENCE.md)
   - Include request/response examples

2. **Update README**
   - Add to features list if significant
   - Update screenshots if UI changed

3. **Add Code Comments**
   - Explain complex logic
   - Document function parameters
   - Add usage examples

## Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add nutrition plan generation service"
git commit -m "Fix: Resolve workout completion bug"
git commit -m "Docs: Update API reference for chat endpoints"

# Bad
git commit -m "fixes"
git commit -m "update stuff"
git commit -m "asdf"
```

**Format:**
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## Feature Request Process

1. **Open an issue** with label `enhancement`
2. **Discuss the feature** with maintainers
3. **Wait for approval** before starting work
4. **Submit PR** when ready

## Code Review Process

All PRs must be reviewed before merging:

1. **Automated checks** must pass
2. **At least one approval** from maintainer
3. **All comments addressed**
4. **No merge conflicts**

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation updates
- Performance impact
- Security considerations

## Branch Naming

Use descriptive branch names:

```bash
feature/workout-video-integration
fix/nutrition-calculation-bug
docs/api-reference-update
refactor/auth-service
```

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Open an issue
- **Chat**: Join our Discord server
- **Email**: contribute@transformers.app

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked in our documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Transformers! 🎉
