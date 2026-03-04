---
description: Run the full development environment using Docker Compose
---
1. Ensure Docker is running.
2. Run the following command to start both backend and frontend:
// turbo
```powershell
docker-compose up -d --build
```
3. Check the logs if needed:
```powershell
docker-compose logs -f
```
