import anyio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from user.router import router


# 쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield                                                           
    # yield 기준으로 앞부분은 서버 실행중 뒷부분은 서버 종료 후에 사용하는 옵션


app = FastAPI(lifespan=lifespan)
app.include_router(router)