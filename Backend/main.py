from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="BrightMinds API")

# Supabase client setup
supabase_url = "https://hupwxuuqqwvaoswnhtmi.supabase.co"
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

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

@app.get("/courses", tags=["courses"])
async def get_courses():
    try:
        response = supabase.table('courses').select("*").execute()
        return {"courses": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses/{course_id}", tags=["courses"])
async def get_course(course_id: str):
    try:
        response = supabase.table('courses').select("*").eq('id', course_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"course": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/courses", tags=["courses"])
async def create_course(course: dict):
    try:
        response = supabase.table('courses').insert(course).execute()
        return {"message": "Course created successfully", "course": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)