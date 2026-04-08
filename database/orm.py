# 2번
# pydantic 같은거

from sqlalchemy.orm import DeclarativeBase

# DeclarativeBase를 그대로 상속받아서 쓴다. 나중에 옵션 조절 가능하지만 지금은 그냥 쓴다.
class Base(DeclarativeBase):
    pass
