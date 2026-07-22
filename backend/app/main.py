from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import coffeebean
from app.routes import coffeebean
from app.routes import brew
from app.routes import analytics
from app.routes import dial_in_session

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="pourover brain",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coffeebean.router)
app.include_router(brew.router)
app.include_router(analytics.router)
app.include_router(dial_in_session.router)

@app.get("/")
def root():
    return {
        "message": "pourover brain is thinking!"
    }