# Reflection

## Key experiences

- Building authentication first made it easier to protect the calculation endpoints consistently.
- Using SQLAlchemy relationships kept the user-to-calculation ownership model simple and testable.
- Writing integration tests against a real temporary database helped catch both validation and auth issues.

## Challenges

- Coordinating JWT auth with FastAPI dependencies required careful setup so tests could override the database cleanly.
- Handling invalid calculation input needed both schema validation and runtime checks for cases like division by zero.
- Preparing CI/CD for Docker Hub required keeping secrets out of the repository while still documenting the deployment flow.
