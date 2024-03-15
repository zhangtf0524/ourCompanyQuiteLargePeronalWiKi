from fastapi import APIRouter
from db.sqliteOperation import Sqlite3Database
from pydantic import BaseModel
from typing import Optional
import sqlite3
import datetime

wikiZone = APIRouter(prefix="/wikiZone", tags=["知识库管理"])


class zoneType(BaseModel):
    userID: int
    zoneName: str
    createTime: Optional[str] = datetime.datetime.now()
    modifyTime: Optional[str] = None
    isDelete: Optional[int] = 0
    comment: Optional[str] = None


@wikiZone.get("/info", summary="查询用户ID对应的知识库信息")
def wikiZoneInfo(userID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    result = conn.select_data("wikiZone", None, f"userID='{userID}' and isDelete = 0")
    return result


@wikiZone.post("/add", summary="新增知识库")
def wikiZoneAdd(wikiZoneAddInfo: zoneType):
    wikiZoneAddInfo = wikiZoneAddInfo.dict()
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    pre_res = conn.select_data(
        "wikiZone",
        "zoneID,zoneName",
        f'userID="{wikiZoneAddInfo["userID"]}" AND zoneName="{wikiZoneAddInfo["zoneName"]}"',
    )
    if pre_res:
        zoneID = dict(pre_res[0])["zoneID"]
        zoneName = dict(pre_res[0])["zoneName"]
        return {
            "errorCode": "0",
            "msg": "kb exists",
            "requestId": "",
            "result": {"kbId": zoneID, "kbName": zoneName},
        }
    else:
        conn.insert_data("wikiZone", wikiZoneAddInfo)
    res = conn.select_data(
        "wikiZone",
        "zoneID,zoneName",
        f'userID="{wikiZoneAddInfo["userID"]}" AND zoneName="{wikiZoneAddInfo["zoneName"]}"',
    )
    zoneID = dict(res[0])["zoneID"]
    zoneName = dict(res[0])["zoneName"]
    return {
        "errorCode": "0",
        "msg": "SUCCESS",
        "requestId": "",
        "result": {"kbId": zoneID, "kbName": zoneName},
    }


@wikiZone.delete("/delete", summary="删除知识库")
def wikiZoneDelete(zoneID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "wikiZone",
        {"isDelete": "1", "modifyTime": datetime.datetime.now()},
        f"zoneID='{zoneID}'",
    )
    return {"message": 200}


@wikiZone.put("/zoneRename", summary="重命名知识库")
def wikiZoneRename(zoneID: int, newName: str):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "wikiZone",
        {"zoneName": newName, "modifyTime": datetime.datetime.now()},
        f"zoneID='{zoneID}'",
    )
    return {"message": 200}
