# Capstone AI-Based Secure Compiler Assistant

## Run the Compiler Backend and UI Together

1. Start the Python backend compiler API:

```bash
python api_server.py
```

2. Start the frontend UI:

```bash
cd ui_for_capstone
npm run dev
```

3. Open the web UI at the URL shown by Next.js (usually `http://localhost:3000`).

4. The UI is already wired to the backend via `ui_for_capstone/app/api/analyze/route.ts`.
   - It forwards analysis requests to `http://127.0.0.1:5000/api/analyze` by default.
   - If needed, set `BACKEND_API_BASE_URL` in `ui_for_capstone/.env.local`.

## Notes

- The backend now auto-detects input language and translates Python, C/C++, and JavaScript into SecureLang before analysis.
- The UI sends code to the proxy route at `/api/analyze`, so the compiler backend remains separated from the frontend.
