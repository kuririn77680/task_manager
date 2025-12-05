Task Manager — Quick Start

1) Install dependencies
- Ensure you have Poetry installed (https://python-poetry.org/)
- From the project root, install deps:
  
  ```bash
  poetry install
  ```

2) Start local PostgreSQL database (Docker):
```bash
docker run -d \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=backend_db \
  -p 5432:5432 postgres:14.5
```

3) Apply database migrations
- Move into the backend folder:
  
  ```bash
  cd backend
  ```
- Run migrations:
  
  ```bash
  poetry run python manage.py migrate
  ```

4) Start the application
```bash
poetry run python manage.py runserver
```

Notes
- Default DB settings are configured for local Docker Postgres in `backend/backend/settings.py`

5) ENDPOINTS

-http://127.0.0.1:8000/api/todos/  -> CRUD

-http://127.0.0.1:8000/api/notes/  -> CRUD