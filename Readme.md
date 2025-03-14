# KtGpt

KtGpt is an application for retrieving knowledge for problems faced earlier and saving solutions for future reference.

## Possible Use Cases

1. **Team Onboarding**: New team members can search the dashboard to understand common problems they will encounter, based on issues documented by existing team members.
2. **Learning Aid**: When you've solved a problem before but can't remember the exact solution, KtGpt helps you find your previous solution instead of searching the internet again.

## Architecture

- **Frontend**: React with TypeScript and Tailwind CSS
- **Backend**: Python FastAPI service with semantic search capabilities
- **Database**: Supabase with PostgreSQL and pgvector extension for similarity search

## Requirements

- Node.js and npm
- Python 3.10+
- Supabase account

## Getting Started

### Setting up Supabase

1. Create a Supabase account at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Enable the pgvector extension in your Supabase project (SQL Editor → Extensions → vector)
4. Run the migration SQL in `supabase/migrations/20250221165224_aged_shore.sql` to set up tables and policies

### Running Locally

1. **Configure environment variables**:
   - Create a `.env` file in the `app` directory with:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   SUPABASE_DB_URL=postgres://postgres:password@db.your-project-id.supabase.co:5432/postgres
   ```

2. **Start the Python API service**:
   ```bash
   # Copy the example environment file
   cp app/.env.example app/.env
   # Edit the app/.env file with your configuration

   # Install requirements
   cd app
   pip install -r requirements.txt
   
   # Start the server
   python main.py
   
   # Or use npm script
   npm run server
   ```

3. **Start the frontend**:
   ```bash
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

## API Endpoints

- `POST /api/problems` - Create a new problem
- `GET /api/problems/search?query={query}` - Search for problems

## Development

- **Build Frontend**: `npm run build`
- **Lint Code**: `npm run lint`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.