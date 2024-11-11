from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/users')
async def all_users() -> list:
    return users

@app.post('/user/{username}/{age}', response_model=User)
async def add_user(username: str = Path(min_length=3, max_length=18, description='Enter your username'),
                   age: int = Path(ge=0, le=120, description='Enter your age')) -> User:
    user_id = len(users) + 1
    user = User(id= user_id, username = username, age = age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username: str = Path(min_length=3, max_length=18, description='Enter new username'),
                      age: int = Path(ge=0, le=120, description='Enter new age')):
    try:
        user = users[user_id - 1]
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int):

    try:
        user = users.pop(user_id-1)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")










