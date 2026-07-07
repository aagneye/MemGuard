# MemGuard Production Setup (Google Auth + Dashboard + Teams)

This guide sets up the current production-facing flow:

- Landing page with Google Sign-In
- Auth verification API
- Dashboard with memory operations
- Team creation and member invite APIs

## 1) Google OAuth Console Setup

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create/select a project.
3. Go to **APIs & Services -> OAuth consent screen** and configure app details.
4. Go to **Credentials -> Create Credentials -> OAuth client ID**.
5. Select **Web application**.
6. Add authorized JavaScript origins:
   - `http://localhost:3000`
   - your production frontend domain
7. Copy the generated **Client ID**.

## 2) Environment variables

Set these in root `.env`:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
GOOGLE_CLIENT_ID=<google-web-client-id>
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<google-web-client-id>
```

Notes:
- `NEXT_PUBLIC_GOOGLE_CLIENT_ID` is used in frontend Google widget init.
- `GOOGLE_CLIENT_ID` is used by backend token verification.
- If `GOOGLE_CLIENT_ID` is empty, backend uses a demo fallback profile.

## 3) Run backend

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4) Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## 5) Validate end-to-end

1. Open landing page.
2. Click Google sign-in.
3. Confirm redirect to `/dashboard`.
4. Create a team from drawer.
5. Invite a member email.
6. Send a chat message and verify memory events update.

## 6) Core production APIs now exposed

- `POST /auth/google/verify`
- `GET /auth/me`
- `POST /chat`
- `GET /memories`
- `POST /memories/{id}/resolve`
- `GET /events`
- `GET /sessions/{session_id}/turns`
- `DELETE /sessions/{session_id}`
- `POST /teams`
- `GET /teams`
- `POST /teams/{team_id}/invite`
- `POST /teams/{team_id}/members`

## 7) Recommended next hardening pass

- Replace in-memory auth/team/memory stores with Postgres + Redis.
- Add role-based team permissions and invite acceptance flow.
- Add API key auth for external enterprise memory-layer integration.
- Add rate limits and request/response audit logging.
- Add CI tests for auth and teams endpoints.
