# Contributing to FinPulse

Thank you for contributing to FinPulse! To ensure a highly professional and clean codebase, please adhere to the following contribution guidelines.

## Branching Strategy

- `main`: Production-ready branch.
- `develop`: Integration branch for new features.
- `feature/*`: Development branches for new features (e.g., `feature/news-scraper`).
- `fix/*`: Bug fix branches (e.g., `fix/api-validation-error`).

## Commit Convention

We follow the **Conventional Commits** standard:

- `feat: ...` for a new feature.
- `fix: ...` for a bug fix.
- `docs: ...` for documentation changes.
- `style: ...` for code formatting, semicolons, etc.
- `refactor: ...` for restructuring code.
- `test: ...` for adding or improving tests.
- `chore: ...` for updating dependencies or build files.

## Code Style Standards

- **Backend:** Follow PEP 8 guidelines. Use type hints for all public functions, include Google-style docstrings, and leverage `ruff` and `black` for formatting.
- **Frontend:** Write clean TypeScript using React Hooks and Next.js App Router. Use Prettier and ESLint for style checks.
- **Database:** All schema changes must be processed through Alembic migrations.
