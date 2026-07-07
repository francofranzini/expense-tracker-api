---
name: expense-tracker
description: Skill for working with the Expense Tracker API (FastAPI + PostgreSQL project). Covers project context, Franco's communication style, decision making process, development principles, code style, git workflow, and common commands.
license: MIT
compatibility: opencode
metadata:
  audience: developer
  project: expense-tracker-api
  language: es-en
---

## Project Context

This is a REST API for expense tracking, built with FastAPI and PostgreSQL.
It's being developed as both a portfolio project and a future SaaS product.
The developer (Franco) is a CS student and IT Analyst learning backend development.

### Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Auth:** JWT via python-jose + bcrypt via passlib
- **Testing:** pytest + TestClient
- **Deploy:** Railway
- **Python:** 3.11 (WSL Ubuntu on Windows)

### Roadmap (next features)
- Pagination on GET /expenses
- CSV export
- Rate limiting
- Multi-currency support (ARS/USD)
- PDF report generation
- Docker
- CI/CD with GitHub Actions
- API keys for external clients

## How to Work With Franco

### Communication Style
- **Explain everything you do before doing it.** Franco wants to understand each change, not just see the result.
- **Use simple language.** Avoid jargon unless you explain it first.
- **When Franco asks "why", give the real reason**, not a surface-level answer.
- **Spanish for discussion, English for code and commits.**

### Decision Making
- **STOP and ask Franco before:**
  - Changing the project structure or architecture
  - Adding new dependencies
  - Modifying existing endpoints or schemas
  - Choosing between two valid approaches
  - Any change that affects how the API works from the user's perspective
- **You CAN proceed without asking for:**
  - Fixing typos or formatting
  - Adding type hints
  - Improving error messages
  - Writing tests for existing functionality

### Development Principles
- **One thing at a time.** Don't change 5 files in one shot. Small, incremental changes.
- **Test everything.** Every new feature needs at least one test.
- **Commit often.** Small, descriptive commits following conventional commits (feat:, fix:, test:, chore:, docs:).
- **Don't break what works.** Run tests before and after changes.
- **No magic.** If a solution is clever but hard to understand, choose the simpler one.

### Code Style
- Python indent: 4 spaces (PEP 8 standard)
- Use type hints where possible
- Docstrings for functions that aren't self-explanatory
- Keep functions short — if a function does more than one thing, split it

### Git Workflow
- Branch: main (direct push for now)
- Commit messages: conventional commits in English
- Always run `pytest` before pushing
- Update `requirements.txt` when adding dependencies

### Project Structure
```
expense-tracker-api/
├── app/
│   ├── main.py          # App entry point
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT authentication
│   └── routers/
│       ├── expenses.py  # Expense endpoints
│       └── users.py     # User endpoints
├── tests/
│   ├── conftest.py      # Test fixtures
│   ├── test_users.py    # User tests
│   └── test_expenses.py # Expense tests
├── .env                 # Environment variables (not in git)
├── requirements.txt
├── Procfile             # Railway deployment
└── CLAUDE.md            # This file
```

### Environment Variables
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_tracker
SECRET_PASSKEY=your_secret_key
```

### Common Commands
```bash
# Run the server
uvicorn app.main:app --reload

# Run tests
pytest -v

# Format code
black app/

# Freeze dependencies
pip freeze > requirements.txt
```
