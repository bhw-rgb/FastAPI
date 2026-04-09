# 1번
# SQLAlchemy를 이용해서 DB와 연결하는 코드

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속 정보
DATABASE_URL = "sqlite:///./local.db"

# Engine: DB와 접속을 관리하는 객체

engine = create_engine(DATABASE_URL, echo=True)     # echo=True -> DB랑 연결되는 동안 SQL 코드를 출력해준다.(개발용, 학습용)


# Session: 한 번의 DB 요청-응답 단위 (Tranjection)
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지 옵션을 정할 수 있다.
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
) 

# session = SessionFactory()

# <SQLAlchemy Dependency Injection>

# 세션을 관리하는 함수
def get_session():
    session = SessionFactory()
    try:
        yield session               # router에서 호출하면 session 반환했다가 일 끝나면 종료
    finally:
        session.close()
