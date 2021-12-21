from routers import ml
from fastapi import FastAPI

app = FastAPI()
app.include_router(ml.router)


@app.get("/")
async def root():
    return {"message": "success"}
