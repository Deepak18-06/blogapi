from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import os
from models import User, BlogPost, BlogPostInDB, UserInDB
from auth import create_access_token, decode_access_token, get_password_hash, verify_password

load_dotenv()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# Database Connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.blog

def get_user(username: str):
    return db.users.find_one({"username": username})

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user["hashed_password"]):
        return UserInDB(username=user["username"], hashed_password=user["hashed_password"])
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB(**user)

# API Endpoints

@app.post("/api/register")
async def register(user: User):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db.users.insert_one({"username": user.username, "hashed_password": hashed_password})
    return {"msg": "User registered successfully"}

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/blogs")
async def get_blogs(current_user: User = Depends(get_current_user)):
    blogs = list(db.blogs.find())
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
    return blogs

@app.get("/api/blogs/{id}")
async def get_blog(id: str, current_user: User = Depends(get_current_user)):
    blog = db.blogs.find_one({"_id": ObjectId(id)})
    if blog:
        blog["_id"] = str(blog["_id"])
        return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/api/blogs")
async def create_blog(blog: BlogPost, current_user: User = Depends(get_current_user)):
    blog_dict = blog.dict()
    blog_dict["author"] = current_user.username
    result = db.blogs.insert_one(blog_dict)
    blog_dict["_id"] = str(result.inserted_id)
    return blog_dict

@app.put("/api/blogs/{id}")
async def update_blog(id: str, blog: BlogPost, current_user: User = Depends(get_current_user)):
    existing_blog = db.blogs.find_one({"_id": ObjectId(id)})
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if existing_blog["author"] != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog")
    db.blogs.update_one({"_id": ObjectId(id)}, {"$set": blog.dict()})
    return {"msg": "Blog updated successfully"}

@app.delete("/api/blogs/{id}")
async def delete_blog(id: str, current_user: User = Depends(get_current_user)):
    existing_blog = db.blogs.find_one({"_id": ObjectId(id)})
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if existing_blog["author"] != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog")
    db.blogs.delete_one({"_id": ObjectId(id)})
    return {"msg": "Blog deleted successfully"}
