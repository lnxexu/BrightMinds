from fastapi import FastAPI
from schema.database import SessionLocal, engine
from schema.models import Base
from routers import users
from fastapi.middleware.cors import CORSMiddleware
from schema.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add this at the bottom of your existing main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)