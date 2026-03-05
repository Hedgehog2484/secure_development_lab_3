import time
import hashlib

from fastapi import FastAPI, Query, HTTPException
from collections import deque

app = FastAPI()


USERS_DB = {  # Пример БД.
    "admin": {
        "hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        "salt": "a1b2c3d4e5f6",
        "fails": deque(maxlen=5),
        "lock": 0,
        "avatar": "/avatar.jpg"
    }
}

@app.get("/login")
def login(username: str = Query(...), password: str = Query(...)):
    u = username
    if u not in USERS_DB: 
        _fail(u)
        return {"success": False, "message": "Invalid credentials"}
    
    user = USERS_DB[u]
    if time.time() < user["lock"]:
        raise HTTPException(429, "Account locked")
    
    if hashlib.sha256((password + user["salt"]).encode()).hexdigest() != user["hash"]:
        _fail(u)
        return {"success": False, "message": "Invalid credentials"}
    
    user["fails"].clear()
    user["lock"] = 0
    return {"success": True, "message": f"Welcome, {u}", "avatar": user["avatar"]}

def _fail(u):
    user = USERS_DB[u]
    now = time.time()
    user["fails"].append(now)
    if len([t for t in user["fails"] if now-t < 900]) >= 5:
        user["lock"] = now + 300


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
