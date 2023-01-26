from fastapi import FastAPI
from app.db import engine, Base
from app.api.api_v1 import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router,)

if __name__ == "__main__":
    import uvicorn # type: ignore

    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
