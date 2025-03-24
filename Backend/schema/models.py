from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Integer, String, Text, TIMESTAMP, Boolean, Date, DateTime, Enum, Float
import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

Base = declarative_base()

class Course(Base):  
    __tablename__ = 'courses'  

    # Define columns  
    course_id = Column(Integer, primary_key=True, autoincrement=True)  
    title = Column(String(255), nullable=False)  
    description = Column(Text, nullable=False)  
    duration = Column(String(50), nullable=False)  
    student_count = Column(Integer, nullable=True)  
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


class User(Base):  
    __tablename__ = 'users'  

    # Define columns  
    user_id = Column(Integer, primary_key=True, autoincrement=True)  
    full_name = Column(String(255), nullable=False)  
    email = Column(String(255), unique=True, nullable=False)  
    password_hash = Column(String(255), nullable=False)  
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    last_login = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=True)

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    error_message: Optional[str] = None
    user: Optional[UserResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Define an Enum for the question types  
class QuestionType(str, enum.Enum):
    multiple_choice = "Multiple Choice"
    true_false = "True/False"
    short_answer = "Short Answer"

class Question(Base):
    __tablename__ = 'questions'
    
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
