from fastapi import FastAPI
from app.api.api_v1 import api_router
from app.api.api_htmx_v1 import htmx_router
from app.auth.router import auth_router
from app.config import settings
from app.auth.db import create_db_and_tables
app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


app.include_router(api_router)
app.include_router(htmx_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn # type: ignore

    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
