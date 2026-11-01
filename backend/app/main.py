from fastapi import FastAPI

from api.middleware import setup_middleware
from api.endpoints import health, prediction


app = FastAPI(title="Cats vs Dogs API")

# Middleware 등록
setup_middleware(app)

# Endpoint 등록
app.include_router(health.router)
app.include_router(prediction.router)