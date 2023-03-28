from pydantic import BaseModel, Field
from typing import Optional

class CreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50) 
    email: str = Field(...,min_length=3, max_length=50)
    mobile: str = Field(...,min_length=3, max_length=50)
    password: str = Field(...,min_length=8, max_length=16)
    username: str = Field(...,min_length=3, max_length=50)
    
class LoginSchema(BaseModel):
    email: str = Field(...,min_length=3, max_length=50)
    password: str = Field(...,min_length=8, max_length=16)
    
class UpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50) 
    email: Optional[str] = Field(None,min_length=3, max_length=50)
    mobile: Optional[str] = Field(None,min_length=3, max_length=50)
    
class CreateBlog(BaseModel):
    title: str = Field(..., min_length=3, max_length=50) 
    description: str = Field(..., min_length=3, max_length=500)
    
class UpdateBlog(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50) 
    description: Optional[str] = Field(None,min_length=3, max_length=500)
    
    class Config:
        orm_mode = True
    
class Person(BaseModel):
    name: str
    email: Optional[str] = None
    mobile: Optional[str]
    username: Optional[bool] = None
    
class JWT(BaseModel):
    sub: str  # Subject (user id)
    exp: int  # Expiration time (Unix timestamp)
    
class SystemUser(BaseModel):
    name: str
    email: str 
    mobile: str 
    username: str 
    
    class Config:
        orm_mode = True