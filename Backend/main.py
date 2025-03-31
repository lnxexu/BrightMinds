from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from passlib.hash import bcrypt

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

# Models
class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    created_at: datetime

@app.get("/")
async def root():
    return {"message": "Welcome to BrightMinds API"}

@app.get("/login/{email}/{password}", tags=["auth"])
async def login(email: str, password: str):
    try:
        # Get user by email and password directly
        response = supabase.table('users').select("*").eq('email', email).eq('password_hash', password).execute()
        
        # Check if any user was found
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = response.data[0]  # Get the first user since email should be unique
        
        # Return user data without password
        return {
            "user": {
                "user_id": user['user_id'],
                "full_name": user['full_name'],
                "email": user['email'],
                "created_at": user['created_at']
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: int):
    try:
        response = supabase.table('users').select("""
            user_id,
            full_name,
            email,
            created_at,
            socialaccounts (
                provider,
                unique_id
            )
        """).eq('user_id', user_id).single().execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {"user": response.data}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

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

@app.post("/sample-data", tags=["admin"])
async def insert_sample_data():
    try:
        # Sample courses data
        courses = [
            {
                "title": "Introduction to Python Programming",
                "description": "Learn the fundamentals of Python programming language including variables, data types, control structures, functions, and object-oriented programming.",
                "duration": "8 weeks",
                "student_count": 25
            },
            {
                "title": "Web Development with React",
                "description": "Master modern web development using React.js. Topics include components, state management, hooks, routing, and connecting to backend APIs.",
                "duration": "12 weeks",
                "student_count": 30
            },
            {
                "title": "Data Science Fundamentals",
                "description": "Introduction to data science concepts including data analysis, visualization, statistical methods, and machine learning basics using Python libraries.",
                "duration": "10 weeks",
                "student_count": 20
            }
        ]
        
        # Insert courses
        response = supabase.table('courses').insert(courses).execute()
        
        return {
            "message": "Sample data inserted successfully",
            "courses": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)