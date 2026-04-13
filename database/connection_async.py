# 1번
# SQLAlchemy를 이용해서 DB와 연결하는 코드

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker                  # 비동기 엔진 불러오기

# 데이터베이스 접속 정보
DATABASE_URL = "sqlite+aiosqlite:///./local.db"                         # 비동기 sqlite 같이 쓰겠다.

# Engine: DB와 접속을 관리하는 객체

async_engine = create_async_engine(DATABASE_URL, echo=True)             # echo=True -> DB랑 연결되는 동안 SQL 코드를 출력해준다.(개발용, 학습용)


# Session: 한 번의 DB 요청-응답 단위 (Tranjection)              
AsyncSessionFactory = async_sessionmaker(                               # 비동기 세션                                                                 
    bind=async_engine,
    # 데이터를 어떻게 다룰지 옵션을 정할 수 있다.
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
) 

# <SQLAlchemy Dependency Injection>

# 세션을 관리하는 함수
async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session               # router에서 호출하면 session 반환했다가 일 끝나면 종료
    finally:
        await session.close()