from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field


app = FastAPI(
    title="Task 5 FastAPI JWT Microservice",
    description="Secure REST API with JWT authentication",
    version="1.0.0",
)

security = HTTPBearer()

SECRET_KEY = "task5-demo-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

users = {}
items = {}
next_item_id = 1


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class ItemResponse(ItemCreate):
    id: int
    owner: str


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )


def create_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username = payload.get("sub")

        if not username or username not in users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return username

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


@app.get("/")
def root():
    return {"message": "FastAPI JWT Microservice is running"}


@app.post("/register", status_code=201)
def register(user: UserRegister):
    if user.username in users:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    users[user.username] = hash_password(user.password)

    return {
        "message": "User registered successfully",
        "username": user.username,
    }


@app.post("/login")
def login(user: UserLogin):
    hashed_password = users.get(user.username)

    if not hashed_password or not verify_password(
        user.password,
        hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(
    item: ItemCreate,
    current_user: str = Depends(get_current_user),
):
    global next_item_id

    new_item = {
        "id": next_item_id,
        "name": item.name,
        "description": item.description,
        "owner": current_user,
    }

    items[next_item_id] = new_item
    next_item_id += 1

    return new_item


@app.get("/items", response_model=list[ItemResponse])
def list_items(current_user: str = Depends(get_current_user)):
    return [
        item
        for item in items.values()
        if item["owner"] == current_user
    ]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    current_user: str = Depends(get_current_user),
):
    item = items.get(item_id)

    if not item or item["owner"] != current_user:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemCreate,
    current_user: str = Depends(get_current_user),
):
    existing = items.get(item_id)

    if not existing or existing["owner"] != current_user:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    existing["name"] = item.name
    existing["description"] = item.description

    return existing


@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    current_user: str = Depends(get_current_user),
):
    existing = items.get(item_id)

    if not existing or existing["owner"] != current_user:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    del items[item_id]

    return {"message": "Item deleted successfully"}
