from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.events import startup
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

app = FastAPI(title="BrightMinds API")

# Supabase client setup
supabase_url = "https://hupwxuuqqwvaoswnhtmi.supabase.co"
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_key:
    raise ValueError("SUPABASE_KEY environment variable is not set")

print("Supabase URL:", supabase_url)  # Debug log
print("Supabase key length:", len(supabase_key) if supabase_key else 0)  # Debug log without exposing the key

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
    access_token: str

class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/")
async def root():
    return {"message": "Welcome to BrightMinds API"}

@app.post("/users/register", tags=["auth"])
async def register_user(user: UserRegister):
    try:
        # First, create the auth user using Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name
                }
            }
        })
        
        print("Auth response:", auth_response)  # Debug log

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to create user account")

        # Get the next available user_id
        max_id_response = supabase.table('users').select("user_id").order('user_id', desc=True).limit(1).execute()
        next_user_id = 1
        if max_id_response.data and len(max_id_response.data) > 0:
            next_user_id = max_id_response.data[0]['user_id'] + 1

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)

        # Create user in our users table
        new_user_data = {
            "user_id": next_user_id,
            "full_name": user.full_name,
            "email": user.email,
            "created_at": datetime.utcnow().isoformat(),
            "password": hashed_password.decode('utf-8')  # Store as string
        }

        # Insert into public.users table
        response = supabase.table('users').insert(new_user_data).execute()
        print("Users table response:", response)  # Debug log

        # Sign in to get the access token
        auth_signin = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if not auth_signin.session:
            raise HTTPException(status_code=500, detail="Failed to get access token")

        return {
            "message": "Registration successful",
            "user": {
                "user_id": next_user_id,
                "full_name": user.full_name,
                "email": user.email,
                "created_at": new_user_data['created_at'],
                "access_token": auth_signin.session.access_token
            }
        }

    except Exception as e:
        print("Registration error:", str(e))
        if isinstance(e, HTTPException):
            raise e
        if "User already registered" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/login", tags=["auth"])
async def login(user: UserLogin):
    try:
        # Use Supabase Auth for login
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Get user details from public.users table using email
        response = supabase.table('users').select("*").eq('email', user.email).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User data not found")
        
        user_data = response.data[0]
        
        # Verify password
        stored_password = user_data['password'].encode('utf-8')
        if not bcrypt.checkpw(user.password.encode('utf-8'), stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return {
            "user": {
                "user_id": user_data['user_id'],
                "full_name": user_data['full_name'],
                "email": user_data['email'],
                "created_at": user_data['created_at'],
                "access_token": auth_response.session.access_token
            }
        }
    except Exception as e:
        print("Login error:", str(e))
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/users/{user_id}", tags=["users"])
async def get_user(user_id: int):
    try:
        response = supabase.table('users').select("*").eq('user_id', user_id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"user": response.data[0]}
    except Exception as e:
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

# Initialize database schema
async def init_database():
    try:
        # Try to insert a user without password_hash to test if constraint exists
        test_response = supabase.table('users').insert({
            "user_id": 999999,  # Using a high number for test
            "full_name": "Test User",
            "email": "test@example.com",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        print("Schema is already updated")
    except Exception as e:
        if "password_hash" in str(e):
            print("Need to update schema - removing password_hash constraint")
            try:
                # Use raw SQL through RPC to alter the table
                result = supabase.rpc(
                    'exec_sql',
                    {
                        'sql_query': """
                        ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;
                        """
                    }
                ).execute()
                print("Schema updated successfully")
            except Exception as e:
                print("Error updating schema:", str(e))
                raise e
        else:
            print("Unexpected error:", str(e))

# Call init_database on startup
@app.on_event("startup")
async def startup_event():
    await init_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)