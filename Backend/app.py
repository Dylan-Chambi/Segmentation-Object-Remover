from fastapi import FastAPI
from src.routers.router import router
from src.config.config import get_settings

SETTINGS = get_settings()


app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.revision)

app.include_router(router, tags=["router"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)