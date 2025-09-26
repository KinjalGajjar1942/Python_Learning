1️⃣ What is FastAPI & Why Async?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use, highly performant, and suitable for production-ready APIs.

Key Features:

Automatic OpenAPI and Swagger documentation.

Built-in data validation using Pydantic.

Asynchronous support using async/await.

Fast execution, often comparable to Node.js and Go.

Why Async?

Async allows your API to handle thousands of concurrent requests efficiently.

Instead of waiting for slow operations (e.g., database or network calls), async functions let the server handle other requests during that wait time.

In FastAPI, async routes are defined with async def:


Why async matters:

Async routes don’t block the server while waiting for I/O operations.

Example: waiting for DB query or external API call.

With sync routes, each request blocks the worker → low concurrenc


uvicorn fastapi_app:app --reload
uvicorn Day4.fastAPIDemo:app --reload


http://127.0.0.1:8000/docs