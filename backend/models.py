from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    isAdmin: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class UserInDB(User):
    password: str

class Tool(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    longDescription: str
    category: str
    pricing: str
    tags: List[str]
    image: str
    url: str
    featured: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ToolCreate(BaseModel):
    name: str
    description: str
    longDescription: str
    category: str
    pricing: str
    tags: List[str]
    image: str
    url: str
    featured: bool = False

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    longDescription: Optional[str] = None
    category: Optional[str] = None
    pricing: Optional[str] = None
    tags: Optional[List[str]] = None
    image: Optional[str] = None
    url: Optional[str] = None
    featured: Optional[bool] = None

class ToolSubmission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    longDescription: str
    category: str
    pricing: str
    tags: List[str]
    imageUrl: str
    url: str
    submitterEmail: EmailStr
    status: str = "pending"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ToolSubmissionCreate(BaseModel):
    name: str
    description: str
    longDescription: str
    category: str
    pricing: str
    tags: str  # comma-separated string from frontend
    imageUrl: str
    url: str
    submitterEmail: EmailStr

class Favorite(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    toolId: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
