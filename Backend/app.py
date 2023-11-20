from fastapi import FastAPI


app = FastAPI(title="Clasts Prediction API")

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)