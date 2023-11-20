from fastapi import FastAPI
from src.routers.router import router


app = FastAPI(title="Clasts Prediction API")

app.include_router(router, tags=["router"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)