# Pydantic 복습
from fastapi import FastAPI, Path, Query, status, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello FastAPI"}

# Path Parameter
@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {"user_id": user_id}

@app.get("users/{user_id}")
def get_user(user_id: int = Path(..., ge=1, description="유저 ID (1 이상)")):
    return {"user_id": user_id}

# Query Parameter
# https://example.com/search?q=fastapi&limit=10
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"q":q, "limit":limit}

# https://example.com/search?q=fastapi&limit=10
@app.get("/search")
def search(
    q: str = Query(
        ...,
        min_length=2,
        max_length=30,
        description="q값 (2 이상)"
        ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="limit 값 (1 이상)")
        ):
    return {"q":q, "limit": limit}

@app.get("/users/{user_id}/posts")
def list_posts(
    user_id: int = Path(
        ...,
        ge=1,
        description="유저 ID (1 이상)"
        ),
    fastapi: str = Query(
        ...,
        min_length=2,
        max_length=20
        ),
    limit: int = Query(
        ...,
        ge=1,
        description="limit (1 이상)")
        ):
    return {"user_id":user_id, "fastapi": fastapi, "limit": limit}

# Optional Type Hints
name: str | None = None
name = "alex"

# Request Body 중첩 모델
class User(BaseModel):
    id: int
    name: str

class Item(BaseModel):
    name: str
    price: int
    description: str | None=None

class Order(BaseModel):
    user: User
    item: Item
    amount: int

@app.post("/orders")
def create_order(order: Order):
    return order

# Request / Response 모델
class ItemCreateRequest(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., ge=0)

class ItemUpdateRequest(BaseModel):
    name: str | None = None
    price: int | None = None
    
class ItemResponse(BaseModel):
    id: int
    name: str
    price: int


# CRUD 실습
# 임시 데이터
users = [{1:"alex", 2:"brook", 3:"charlie"}]
items = [{"apple":1000, "banana":2000, "cherry":3000}]
stored_item = [
    "apple",
    "banan",
    "cherry",
    "dragon fruit",
    "eggplant",
    "fig",
    "grape",
    "honeydue",
    "indian fig",
    "jujube",
    "kiwi",
    "lemon",
    "mango",
    "nectarine",
    "orange",
    "peach",
    "quince",
    "raspberry",
    "strawberry",
    "tangerine",
    "ugly fruit",
    "velvet apple",
    "watermelon",
    "xigua",
    "yuju",
    "zucchini"]

# [1] Create
@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK
    )
def create_item(body: ItemCreateRequest):
    new_item = {
        "id":len(items)+1,
        "name": body.name,
        "price": body.price,
    }
    items.append(new_item)
    return new_item

# [2] Read
@app.get(
    "/items",
    response_model=list[ItemResponse]
    )
def list_items():
    return items

# [3] Read: item 단일 조회
@app.get(
    "/items/{item_id}",
    response_model=ItemResponse
    )
def get_read_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item is not found")

# [4] Uptate: item 부분 수정
@app.patch(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED
    )
def patch_item(
    item_id: int,
    body: ItemUpdateRequest,
    ):
    for item in items:
        if item["id"] == item_id:
            if body.name is not None:
                stored_item["id"] = body.name
            if body.price is not None:
                stored_item["id"] = body.price
            return stored_item
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item is not found")

# [5] Delelte: Item 삭제
@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")