from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_all_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_users(username: str, age: int) -> str:
    user_id = 1
    if users:
        user_id = users[-1].id + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: str, username: str, age: int):
    try:
        for user in users:
            if user.id == user_id:
                user.username, user.age = username, age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: str):
    try:
        for user in users:
            if user_id == user.id:
                users.remove(user)
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')
