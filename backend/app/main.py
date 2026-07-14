from fastapi import FastAPI
from app.database import engine, Base
from app.models import coffeebean
from app.routes import coffeebean

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="pourover brain",
    version="0.1"
)

app.include_router(coffeebean.router)

@app.get("/")
def root():
    return {
        "message": "pourover brain is thinking!"
    }