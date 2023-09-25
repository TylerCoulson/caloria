from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from app.config import settings
from app.api.api_v1 import api_router
from app.api.api_htmx_v1 import htmx_router
from app.db import engine, Base

app = FastAPI(title=settings.APP_NAME)


app.mount("/static", StaticFiles(directory="static"), name="static")

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(api_router)
app.include_router(htmx_router)

@app.exception_handler(HTTPException)
async def exception_404(request: Request, exc:HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
    if exc.detail == "Profile Not Found":
        return RedirectResponse('/create_profile')
    else:
        return RedirectResponse('/not_found')
    


if __name__ == "__main__":
    import uvicorn # type: ignore

    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
