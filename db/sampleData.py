from fastapi import APIRouter
from db.sqliteOperation import Sqlite3Database
from pydantic import BaseModel
from typing import Optional
import sqlite3
import datetime

sampleData = APIRouter(prefix="/sampleData", tags=["知识库数据样例"])


class sampeDataType(BaseModel):
    fileID: int
    dataText: str
    splitNum: int
    createTime: Optional[str] = datetime.datetime.now()
    modifyTime: Optional[str] = None
    isDelete: Optional[str] = 0
    comment: Optional[str] = None


class sampeDataUpdateType(BaseModel):
    sampleID: int
    dataText: str
    splitNum: int
    modifyTime: Optional[str] = datetime.datetime.now()
    comment: Optional[str] = None


@sampleData.get("/info", summary="查询文件ID对应的样本数据信息")
def sampleDataInfo(fileID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    result = conn.select_data("sampleData", None, f"fileID='{fileID}' and isDelete = 0")
    return result


@sampleData.post("/add", summary="插入样本数据")
def sampleDataAdd(sampleDataAddInfo: sampeDataType):
    sampleDataAddInfo = sampleDataAddInfo.dict()
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.insert_data("sampleData", sampleDataAddInfo)
    return {"message": 200}


@sampleData.delete("/delete", summary="删除样本数据")
def sampleDataDelete(sampleID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "sampleData",
        {"isDelete": "1", "modifyTime": datetime.datetime.now()},
        f"sampleID='{sampleID}'",
    )
    return {"message": 200}


@sampleData.put("/update", summary="更新样本数据")
def sampleDataUpate(sampleDataUpdateInfo: sampeDataUpdateType):
    sampleDataUpdateInfo = sampleDataUpdateInfo.dict()
    sampleID = sampleDataUpdateInfo["sampleID"]
    sampleDataUpdateInfo.pop("sampleID")
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data("sampleData", sampleDataUpdateInfo, f"sampleID='{sampleID}'")
    return {"message": 200}
