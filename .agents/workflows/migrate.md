---
description: Migrate data from ZKTime Lite (SQLite) to PostgreSQL
---
1. Ensure the backend container is running.
2. Execute the migration script:
// turbo
```powershell
docker-compose exec backend python -m app.migrate
```
3. Initialize the admin user:
// turbo
```powershell
docker-compose exec backend python -m app.initial_data
```
