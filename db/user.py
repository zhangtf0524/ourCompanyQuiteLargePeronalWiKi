from fastapi import APIRouter
from db.sqliteOperation import Sqlite3Database
from pydantic import BaseModel
from typing import Optional
import sqlite3
import datetime

user = APIRouter(prefix="/user",tags=["知识库用户管理"])

class userType(BaseModel):
    userName:str
    userPassword:str
    role:Optional[str] = None
    status:Optional[str] = "1"
    registerTime:Optional[str] = datetime.datetime.now()
    mobilePhone:Optional[str] = None
    createTime:Optional[str] = datetime.datetime.now()
    modifyTime:Optional[str] = None
    isDelete:Optional[int] = 0
    comment:Optional[str] = None

@user.get("/info",summary="查询用户所有信息")
def userInfo(userName):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    result = conn.select_data("user",None,f"userName='{userName}' and isDelete = 0")
    return result

@user.post("/add",summary="新增用户")
def userAdd(userInfo:userType):
    userInfo = userInfo.dict()
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.insert_data("user",userInfo)
    
    return {"message":200}



