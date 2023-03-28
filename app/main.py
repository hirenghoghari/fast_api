from fastapi import FastAPI,Depends
from app.schema import CreateSchema, UpdateSchema, CreateBlog, UpdateBlog, LoginSchema, SystemUser
from app.models import session, UserAccount, Blog
from app.utils import get_hashed_password,verify_password, create_access_token
from app.deps import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def user_register(payload: CreateSchema):
    password = get_hashed_password(payload.password)
    user = UserAccount(name=payload.name,email=payload.email,mobile=payload.mobile,password=password,username=payload.username)
    session.add(user)
    session.commit()
    return {"user added": user.email}

@app.post("/login")
async def login(payload: LoginSchema):
    user_query = session.query(UserAccount).filter_by(email=payload.email).first()
    hashed_pass = user_query.password
    if not verify_password(payload.password, hashed_pass):
        return {"message":"Incorrect email or password"}

    return {
        "access_token": create_access_token(user_query.email),
    }
    
@app.get("/get",response_model=SystemUser)
def get_all_useraccount(user: str = Depends(get_current_user)):
    return user
  
@app.put("/user_update/{id}")
def update_useraccount(payload: UpdateSchema,id: int):
    user_query = session.query(UserAccount).get(payload.id)
    if not user_query:
        return {"message": "Invalid user ID"}
    if payload.name:
        user_query.name = payload.name
    if payload.email:
        user_query.email = payload.email
    if payload.mobile:
        user_query.mobile = payload.mobile
    session.add(user_query)
    session.commit()
    return {"message": "Data updated"}
    
@app.delete("/delete/{id}")
def delete_useraccount(id: int,user: str = Depends(get_current_user)):
    user_query = session.query(UserAccount).get(id)
    if user_query:
        session.delete(user_query)
        session.commit()
        return {"message": "user deleted"}
    else:
        return {"message": "please enter valid id"}
    
@app.post("/create_blog")
def create_blog(payload: CreateBlog,user: str = Depends(get_current_user)):
    blog = Blog(title=payload.title,description=payload.description,user_id=int(user.id))
    session.add(blog)
    session.commit()
    return {"message": "blog added"}

@app.get("/my_blog",response_model=List[UpdateBlog])
def get_my_blog(user: str = Depends(get_current_user)):
    blog_obj = user.blogs
    return blog_obj

@app.get("/get_blog/{id}",response_model=UpdateBlog)
def get_one_blog(id: int, user: str = Depends(get_current_user)):
    blog_obj = session.query(Blog).filter_by(id=id,user_id=user.id).first()
    return blog_obj

@app.put("/update_blog")
def update_blog(payload: UpdateBlog):
    blog_obj = session.query(Blog).get(payload.id)
    if not blog_obj:
        return {"message": "Invalid blog ID"}
    if payload.title:
        blog_obj.title = payload.title
    if payload.description:
        blog_obj.description = payload.description
    session.add(blog_obj)
    session.commit()
    return {"message": "your blog update"}
    
@app.delete("/blog_delete")
def delete_blog(id: int):
    blog_obj = session.query(Blog).get(id)
    if not blog_obj:
        return {"message": "Invalid blog ID"}
    session.delete(blog_obj)
    session.commit()
    return {"message":"your blog delete"}