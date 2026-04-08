# 응답 데이터 관리 형식

# 1) 클라이언트에게 잘못된 데이터를 넘기지 않기 위해 -> 반환할 때 필터링을 해서 원하는 값만 반환하게 한다.
# 2) 민감 데이터를 실수로 유출하지 않기 위해

from datetime import datetime
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    job: str
    created_at: datetime