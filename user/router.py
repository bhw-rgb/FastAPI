# 1) DB랑 Session을 진행하기 위해서 SessionFactory 불러온다.
# 2) user.models에서 User를 불러온다. -> User 객체는 DeclarativeBase 상속받음 -> orm은 Python 코드로 SQL에 요청함.
# 3) router에 session을 넣는다(공장) -> user.models에 있는 User 객체를 가져온다
# 4) User 객체는 Python 응답을 SQL로 보내서 데이터를 요청, 응답

from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete

from database.connection import get_session                       # 세션 주입
from database.connection_async import get_async_session           # 비동기 세션 추가
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse


# user 핸들러 함수들을 묶어서 관리하는 객체
router = APIRouter(prefix="/users", tags=["User"])

# GET /users
@router.get(
    "",
    summary="전체 사용자 데이터 조회 API",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse]
    )
async def get_users_handler(session = Depends(get_async_session)):
    # statement = 구문(명령문)
    stmt = select(User)                         # SELECT * FROM user;
    result = await session.execute(stmt)        # execute에 I/O 작업이 발생하시 때문에 await을 넣어준다.
    users = result.scalars().all()              # mappings() -> 딕셔너리로 가져온다. # scalars() -> 맨 첫번째 값만 가져온다.

    return users


# GET /users/search?name=alex
@router.get(
    "/search",
    summary="사용자 데이터 검색 API",
    response_model=list[UserResponse]
    )
async def search_user_handler(
    name: str | None = Query(None), 
    job: str | None = Query(None), 
    session = Depends(get_async_session),
    ):                                          # Depends(get_session) -> SQLAlchemy 의존성 주입
    stmt = select(User)
    if name:
        stmt = stmt.where(User.name == name)
    if job:
        stmt = stmt.where(User.job == job)
    if not name and not job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="검색 조건을 입력해주세요.")
    
    result = await session.execute(stmt)
    users = result.scalars().all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    return users

# GET /users/{user_id}
@router.get(
    "/{user_id}",
    summary="단일 사용자 데이터 조회 API",
    response_model=UserResponse
    )
async def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_async_session),             # Depends(get_session) -> SQLAlchemy 의존성 주입
    ):                                          
    
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()                      # scalar() -> 첫 번째 객체 하나만 줘라. 존재하면 user 객체 존재하지 않으면 None

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user


# POST /users
@router.post(
    "",
    summary="사용자 데이터 추가 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
    )
async def create_user_handler(
    body: UserCreateRequest, 
    session = Depends(get_async_session),             # Depends(get_session) -> SQLAlchemy 의존성 주입
    ):
    new_user = User(name=body.name, job=body.job)
    session.add(new_user)                           # Session 데이터 추가하라고 DB 한테 말함 (등록 예약)
    await session.commit()                                # 변경사항 저장 (진짜 등록)
    await session.refresh(new_user)                       # id, created_at 읽어옴 -> DB랑 FastAPI서버를 동기화한다.
    return new_user


# PATCH /users/{user_id}
@router.patch(
    "/{user_id}",
    summary="사용자 데이터 수정 API",
    response_model=UserResponse,
    )
async def update_user_handler(
    user_id: int, 
    body: UserUpdateRequest, 
    session = Depends(get_session),                         # Depends(get_session) -> SQLAlchemy 의존성 주입
    ):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)                    # SELECT Query
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    user.job = body.job
    await session.commit()                                  # UPDATE Query
    # session.commit은 변경사항 저장 add가 필요 없는 이유? 
    # -> session.execute로 가져왔기 때문에 자동 add 함
    return user



# DELETE /user/{user_id}
# 메세지를 넣어도 204 때문에 메세지 안뜬다.
@router.delete(
    "/{user_id}",
    summary="사용자 데이터 삭제 API",
    status_code=status.HTTP_204_NO_CONTENT,
    )
async def delete_user_handler(
    user_id:int, 
    session = Depends(get_async_session),             # Depends(get_session) -> SQLAlchemy 의존성 주입
    ): 

    # 1) 의존성 주입 전 코드 | 조회하고 삭제하는법
    # with SessionFactory as session:
    #     stmt = select(User).Where(User.id == user_id)
    #     result = session.execute(stmt)
    #     user = result.scalar()

    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
        
    #     session.delete(user)   #-> 객체 삭제.
    #     #session.expunge(user)  -> 객체에 관심을 끈다.
    #     session.commit()

    # 2) 바로 삭제하는법
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)     # 삭제
    await session.commit()          # 확정