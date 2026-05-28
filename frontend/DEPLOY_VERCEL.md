# Frontend deployment (Vercel)

## Files used

- `frontend/vercel.json`
- `frontend/.env.example`
- `frontend/src/api/client.js`

## Deploy

1. Import repository in Vercel.
2. Set project root directory to `frontend`.
3. Set environment variable:
   - `VITE_API_BASE_URL=https://<your-render-backend>/api`
4. Build settings come from `vercel.json`:
   - build command: `npm run build`
   - output directory: `dist`
5. Deploy.
