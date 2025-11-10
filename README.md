# Setup & Local Run Instructions

## Backend (FastAPI)
1. **Pull repo**
   ```bash
   git clone https://github.com/Kuo-Chun-Ting/MetAI-Assignment-BE.git
   cd MetAI-Assignment-BE/be_fastapi
   ```
2. **Install**
   ```bash
   pip install -r requirements.txt
   ```
3. **Supabase setup**
   - Create a Supabase project.
   - Database: make sure to find the **Session Pooler** connection info and use those values in the environment variables below.
   - Storage:
     1. Create a bucket named `files`.
     2. Set the bucket to **public**.
     3. Enable the default “Allow all operations” policies.
     4. Edit each policy and set Definition to `true` so the anon key can read/write.
4. **Environment variables**
   - Create `.env` with (please use your own Supabase/Postgres project):
     ```
     DB_HOST=<your_postgres_host>
     DB_PORT=<your_postgres_port>
     DB_NAME=<your_database_name>
     DB_USER=<your_database_user>
     DB_PASSWORD=<your_database_password>
     JWT_SECRET_KEY=<random_string_for_signing_tokens>
     SUPABASE_URL=<your_supabase_project_url>
     SUPABASE_ANON_KEY=<your_supabase_anon_key>
     ```
5. **Load config**
   ```bash
   set -a && source .env && set +a
   ```
6. **Init database**
   ```bash
   python init_database.py   # run at least once; re-run when you need a clean DB/storage
   ```
7. **Run**
   ```bash
   uvicorn src.app:app --reload
   ```

## Frontend (Vue)
1. **Pull repo**
   ```bash
   git clone https://github.com/Kuo-Chun-Ting/MetAI-Assignment-FE.git
   cd MetAI-Assignment-FE/fe_vue
   ```
2. **Install**
   ```bash
   npm install
   ```
3. **Environment variables**
   - Create `.env.local` (or export before running) with:
     ```
     VITE_API_BASE_URL=http://localhost:8000
     ```
   - For production, set it to the deployed FastAPI URL.
4. **Run**
   ```bash
   npm run dev
   ```

## Architecture and Design Decisions

## High-level
- Frontend: Vue 3 + Vite hosted on Render (Singapore).
- Backend: FastAPI hosted on Render (Singapore).
- Database & Storage: Supabase (Postgres + Storage, Singapore) accessed only via the backend.

### Backend
- 3-layer structure: REST APIs → services → repositories (SQLAlchemy ORM).
- Data access is kept simple: every query filters by `user_id`, no database-level RLS yet.
- No DB versioning/migration tooling because this project is deployed only once for the assignment.
- Auth session state is kept simple: valid tokens live in an in-memory cache and never expire, so restarting the server wipes the cache and everyone must log in again.
- Upload flow is also simple: backend uploads the full file to Supabase first, then writes metadata; frontend waits for the whole process to finish (no background tasks yet).

### Frontend
- Register auto-logs in and lands on the single Home view (upload + list + rename + delete).
- Pagination is set to 3 items per page by default to make manual testing easier.
- Upload progress was kept simple: only the browser → API transfer is tracked, so the bar may reach 100% while the backend is still sending the file to Supabase.
- Thumbnails are kept simple (check extension only); upload a PNG or JPG to see it working.

# Trade-offs or Known Limitations
- Backend is on Render's free plan. It sleeps after 15 minutes of inactivity. Expect a 'cold start' delay of 30-60 seconds for the first request.
- JWT never expire and valid tokens are cached only in memory, so restarting the backend forces everyone to log in again.
- Upload/download progress only covers browser → API transfer; in the live Render environment I can reliably handle up to ~40 MB before the request times out.
- Storage bucket is public and accessed via the anon key; anyone with the URL can read the file.
- No DB migration tooling—changing the schema today means rerunning `init_database.py`, which wipes the existing data.

# Future Improvements
- Add DB migrations/seed scripts so schema changes don’t require wiping data with `init_database.py`.
- Implement proper session lifecycle: token expiry + refresh + a persistent cache so backend restarts don’t force everyone to log in again.
- Strengthen data access: use a private Supabase bucket, service-role key, and RLS/JWT-based policies instead of public/anon access.
- Improve uploads/downloads: chunk uploads plus backend progress updates (WebSocket or polling) so FE sees Supabase write progress.
- Add automated coverage (unit tests, API tests, end-to-end tests).
- Prepare a separate Supabase project/credentials for testing so others can run the app without touching the main data.
