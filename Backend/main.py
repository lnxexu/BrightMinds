from fastapi import FastAPI
from schema.database import SessionLocal, engine
from schema.models import Base
from routers import users, oauth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(oauth.router, prefix="/oauth", tags=["oauth"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to BrightMinds API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)