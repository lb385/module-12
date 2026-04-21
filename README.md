# Module 12 Backend

FastAPI backend with user registration/login, calculation CRUD, integration tests, and CI/CD support.

## Features

- Register users at `POST /users/register`
- Login users at `POST /users/login`
- Create, browse, read, update, and delete calculations at `/calculations`
- JWT auth for calculation endpoints
- OpenAPI docs at `/docs` and `/redoc`

## Local setup

1. Create a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables as needed:

   ```bash
   export DATABASE_URL=sqlite:///./app.db
   export SECRET_KEY=change-me
   ```

4. Run the server:

   ```bash
   uvicorn app.main:app --reload
   ```

## Integration tests

Run the pytest suite:

```bash
pytest
```

The tests cover:

- User registration and login
- JWT-protected calculation CRUD operations
- Validation and error handling

## Manual checks

- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Register a user with `POST /users/register`
- Log in with `POST /users/login`
- Copy the returned bearer token into the Authorize button
- Create, browse, read, update, and delete calculations

## Docker Hub

Replace the placeholder below with your Docker Hub repository:

- Docker Hub repository: `YOUR_DOCKER_HUB_REPOSITORY`

## CI/CD

The GitHub Actions workflow runs tests on each push and pull request. It is also configured to build and push a Docker image to Docker Hub when secrets are provided.
