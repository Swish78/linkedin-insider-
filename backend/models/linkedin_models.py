from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Post(BaseModel):
    id: str = Field(...)
    page_id: str = Field(...)
    content: str = Field(...)
    likes_count: int = Field(default=0)
    comments_count: int = Field(default=0)


class Person(BaseModel):
    id: str = Field(...)
    name: str
    title: Optional[str] = None
    company_id: str = Field(...)


class LinkedInPage(BaseModel):
    id: str = Field(...)
    name: str
    url: str
    profile_picture_url: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    followers_count: int = Field(default=0)
    employee_count: Optional[int] = None
    specialities: List[str] = Field(default_factory=list)
    posts: List[Post] = Field(default_factory=list)
    employees: List[Person] = Field(default_factory=list)
    ai_insights: Optional[str] = Field(None)
