# KtGpt Development Guide

## Build and Run Commands
- Frontend (React): `npm run dev` - Start Vite dev server
- Build: `npm run build` - Build production frontend
- Lint: `npm run lint` - Run ESLint
- Backend API: `npm run server` or `cd app && python main.py`

## Testing
- Frontend: No test commands defined yet
- Backend: No defined test commands yet

## Code Style Guidelines
- TypeScript: Strict mode, no unused locals/parameters
- React: Follow React hooks rules, use functional components
- Python: PEP 8 style guide for Python code
- Error handling: Use proper type checking and validation
- Naming: camelCase for JS/TS, PascalCase for React components, snake_case for Python

## Component Structure
- Frontend: React with TypeScript and Tailwind CSS
- Backend: Python FastAPI service
- Database: Supabase with PostgreSQL and pgvector extension

## Supabase Setup
- Create a Supabase account and project
- Enable pgvector extension in SQL Editor → Extensions
- Run migration in `supabase/migrations/20250221165224_aged_shore.sql`
- Configure environment variables:
  - SUPABASE_URL: Your Supabase project URL
  - SUPABASE_KEY: Your Supabase anon key
  - SUPABASE_DB_URL: Postgres connection string