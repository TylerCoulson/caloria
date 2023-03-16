from fastapi import FastAPI
from app.api.api_v1 import api_router
from app.api.api_htmx_v1 import htmx_router

from app.auth.router import auth_router
from app.config import settings
from app.db import engine, Base

app = FastAPI(title=settings.APP_NAME)




async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


app.include_router(api_router)
app.include_router(htmx_router)


if __name__ == "__main__":
    import uvicorn # type: ignore

    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
