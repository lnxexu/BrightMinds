from fastapi import APIRouter, Depends, HTTPException, status
from schema.database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from schema.models import User, UserCreate, UserResponse
from passlib.context import CryptContext
from sqlalchemy import text



router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# get all users
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserResponse.model_validate(user) for user in users]

@router.post("/users/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = pwd_context.hash(user.password)
        
        # Create new user
        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password_hash=hashed_password,  # Store the hashed password
            created_at=datetime.now(),
            last_login=datetime.now(),
            is_active=True
        )
        
        # Add to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse.model_validate(new_user)

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/users/verify")
def verify_user(email: str, password: str, db: Session = Depends(get_db)):
    # Get user by email using SQLAlchemy ORM instead of raw SQL
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Verify the password against the stored hash
    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
        
    return dict(user.__dict__)