# MetAI File Management API

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
uvicorn src.app:app --reload
```
Docs at `http://localhost:8000/docs`.

## Auth
- Register/Login return an HS256 JWT; send it via `Authorization: Bearer <token>`.
- Tokens live in an in-memory cache for logout support; restarting the API invalidates every token.
- `POST /auth/logout` clears the caller’s cached tokens. Log in again to get a fresh token.
