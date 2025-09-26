from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="User API", version="1.0.0")
db = {}

class User(BaseModel):
    name: str = Field(..., example="Alice")  # example shows in Swagger
    age: int = Field(..., gt=0, example=25) # age must be > 0
    

    
@app.post("/user", response_model=User, status_code=201)
async def create_user(user: User):
    if user.name in db:
        raise HTTPException(status_code=400, detail="User already exists")
    db[user.name] = user
    return user


@app.get("/user/{name}", response_model=User)
async def get_user(name: str = Path(..., description="Name of the user")):
    if name not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[name]

@app.get("/users", response_model=List[User])
async def get_all_users():
    return list(db.values())


@app.delete("/user/{name}", status_code=204)
async def delete_user(name: str):
    if name not in db:
        raise HTTPException(status_code=404, detail="User not found")
    del db[name]
    return None
