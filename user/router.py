# 1) DB랑 Session을 진행하기 위해서 SessionFactory 불러온다.
# 2) user.models에서 User를 불러온다. -> User 객체는 DeclarativeBase 상속받음 -> orm은 Python 코드로 SQL에 요청함.
# 3) router에 session을 넣는다(공장) -> user.models에 있는 User 객체를 가져온다
# 4) User 객체는 Python 응답을 SQL로 보내서 데이터를 만

from fastapi import APIRouter, Path, Query, status, HTTPException

from database.connection import SessionFactory
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse


# user 핸들러 함수들을 묶어서 관리하는 객체
router = APIRouter(prefix="/users", tags=["User"])


# 임시 데이터
users = [
    {"id": 1, "name": "alex", "job": "sw engineer"},
    {"id": 2, "name": "bob", "job": "designer"},
    {"id": 3, "name": "chris", "job": "manager"}
]


# 전체 사용자 조회
# GET /users
@router.get("",status_code=status.HTTP_200_OK)
def get_users_handler():
    return users


# 사용자 정보 검색 API
# GET /users/search?name=alex
@router.get("/search")
def search_user_handler(name: str | None = Query(None), job: str | None = Query(None)):
    if name is None and job is None:
        return {"msg": "조회에 사용할 QueryParam이 필요합니다."}

    for user in users:
        if user["name"] == name:
            return user
        if user["job"] == job:
            return user

    return {"msg": "해당 사용자를 찾을 수 없습니다."}


# 사용자 1명 조회
# GET /users/1
@router.get("/{user_id}")
def get_user_handler(user_id: int = Path(..., ge=1)):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


# 회원 추가 API
# POST /users
@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user_handler(body: UserCreateRequest):

    with SessionFactory as session:
        new_user = User(name=body.name, job=body.job)
        session.add(new_user)       # Session 데이터 추가하라고 DB 한테 말함
        session.commit()            # 변경사항 저장
        session.refresh(new_user)   # id, created_at 읽어옴 -> DB랑 FastAPI서버를 동기화한다.
        return new_user


# 회원 정보 수정 API
# PATCH /users/{user_id}
@router.patch("/{user_id}", response_model=UserResponse)
def update_user_handler(user_id: int, body: UserUpdateRequest):

    for user in users:
        if user["id"] == user_id:
            user["job"] = body.job
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


# 회원 삭제 API
# DELETE /user/{user_id}
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT) # 메세지를 넣어도 204 때문에 메세지 안뜬다.
def delete_user_handler(user_id:int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")