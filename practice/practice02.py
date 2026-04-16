# fast api import-----------------------------
from fastapi import FastAPI
# FastAPI 클래스를 app 변수에 담아 instance 생성
app = FastAPI()
# @something -> decorator
# 데코레이터는 FastAPI에게 아래 함수가 경로 / 의 get 작동에 해당한다고 알려줍니다.
# 이것이 "경로 처리 데코레이터" 입니다.
@app.get("/")
@app.post()
@app.put()
@app.delete()

# "경로 처리 함수 정의"---------------------------
# URL "/" 에 대한 GET 작동을 사용하는 요청을 받을 때마다 FastAPI에 의해 호출됩니다.
def root():

# 콘텐츠 반환    
    return {"message": "Hello World"}

# 타입 힌트 경로 매개변수----------------------------
from fastapi import FastAPI
app = FastAPI()
@app.get("items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# 파이썬 타입을 선언하면 FastAPI는 데이터 검증을 합니다.
# 또한 오류에는 검증을 통과하지 못한 지점이 전확히 명시됩니다.
# 이는 API와 상호 작용하는 코드를 개발하고 디버깅하는 데 매우 유용합니다.

# 경로 처리 순서-------------------------------------
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# /users/me 경로와 /users/{users_id} 경로가 있습니다.
# 경로 처리는 순차적으로 평가되기 때문에 /uesers/me에 대한 경로가 /users/{users_id} 이전에
# 선언 되었는지 확인해야 합니다. 그렇지 않으면 /users/{users_id}에 대한 경로가
# /users/me 에도 매칭되어, 매개변수 user_id에 "me" 값이 들어왔다고 "생각하게" 됩니다.

# 경로 재정의 불가능----------------------------
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def read_users():
    return ["Rick", "Morty"]

@app.get("/users")
def read_users2():
    return ["Bean","Elfo"]

# 사전 정의값---------------------------------
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    # ModelName.lenet.value == "lenet"

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

# 쿼리 매개변수------------------------------------
from fastapi import FastAPI
 
app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name":  "Baz"}]

@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 선택적 매개변수----------------------------------
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# 쿼리 매개변수 타입 변환
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 필수적, 기본적, 선택적 매개변수 정리-------------------
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_user_item(
    item_id:str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item