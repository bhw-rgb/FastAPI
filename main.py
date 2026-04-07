from fastapi import FastAPI, Path, Query

from request import UserCreateRequest
from response import UserRespose


app = FastAPI()

# 임시 데이터
users = [
    {"id": 1, "name": "alex", "job": "developer"},
    {"id": 2, "name": "bob", "job": "designer"},
    {"id": 3, "name": "chris", "job": "manager"},
]

@app.get("/")
def read_root():
    return {"ping": "pong"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello, FastAPI"}

# 전체 사용자 조회
@app.get("/users")
def get_users():
    return users

# 사용자 정보 검색 API
# GET /users/search?name=alex
@app.get("/users/search")
def search_user(name: str | None = Query(None)):
    if name is None:
        return {"msg": "조회에 사용할 QueryParam이 필요합니다."}

    for user in users:
        if user["name"] == name:
            return user

    return {"msg": "해당 사용자를 찾을 수 없습니다."}

# 사용자 1명 조회
# GET /users/1
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return user

    return {"msg": "해당 사용자를 찾을 수 없습니다."}

# 회원 추가 API
# POST /users
@app.post("/users", response_model=UserRespose)
def create_user(body: UserCreateRequest):
    new_user = {
        "id": len(users) + 1,
        "name": body.name,
        "job": body.job,
    }
    users.append(new_user)
    return new_user