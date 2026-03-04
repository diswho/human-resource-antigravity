# Project Instructions & Rules

This file contains the core rules and architectural patterns for the Human Resource Management System. Antigravity will follow these preferences for all code generation and refactoring.

## 🛠️ General Principles
- Use **TypeScript** for all frontend code.
- Use **FastAPI** with **SQLModel** for all backend logic.
- Prefer **functional components** and **hooks** in React.
- Maintain **Role-Based Access Control (RBAC)** across all endpoints.

## 🎨 Frontend (React + Tailwind)
- **Styling**: Always use Tailwind CSS. Favor `shadcn/ui` components when available.
- **State Management**: Use React Context for global state (e.g., `useAuth`). Use `react-query` or similar for server state if introduced.
- **Organization**: Components in `src/components`, pages in `src/pages`, and custom hooks in `src/hooks`.

## ⚙️ Backend (FastAPI)
- **Dependencies**: Use Dependency Injection in `api/deps.py` for database sessions and authentication.
- **Models**: Separate `SQLModel` definitions into `models/` with clear Pydantic schemas for request/response validation.
- **Migrations**: Always consider how changes affect the legacy `ZKTimeNet08.db` migration logic.

## 📝 Documentation
- Keep the `README.md` updated with new environment variables.
- Use JSDoc/Docstrings for complex business logic.
