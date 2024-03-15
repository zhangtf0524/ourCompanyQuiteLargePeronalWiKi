import os
import sqlite3
import datetime
from fastapi import APIRouter, UploadFile
from db.sqliteOperation import Sqlite3Database
from pydantic import BaseModel
from typing import Optional
from llama_index.core import SimpleDirectoryReader
from utils.model_loader import text2vec_model, asr_model
from utils.text_retriever import TextRetriever
from utils.data_extractor import DataExtractor
from zhconv import convert

uploadFiles = APIRouter(prefix="/uploadFiles", tags=["知识库上传文件"])


class uploadFilesType(BaseModel):
    zoneID: int
    fileName: str
    fileType: Optional[str] = None
    status: Optional[str] = None
    fileSize: Optional[str] = None
    filePosition: str
    attributeCode: Optional[str] = None
    createTime: Optional[str] = datetime.datetime.now()
    modifyTime: Optional[str] = None
    isDelete: Optional[str] = 0
    comment: Optional[str] = None


def split_list(text, length=100):
    return [text[i : i + length] for i in range(0, len(text), length)]


def use_knn(zoneID, fileID, fileType):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    knn_file_path = "/data/personal_wiki/assets/" + str(zoneID) + ".bin"
    ret = TextRetriever(knn_file_path, text2vec_model)
    res_list = conn.select_data(
        "sampleData", "dataText, sampleID", 'fileID="' + str(fileID) + '"'
    )
    # print(len(res_list))
    text_list = []
    id_list = []
    for i in range(0, len(res_list)):
        text_list.append(dict(res_list[i])["dataText"])
        id_list.append(dict(res_list[i])["sampleID"])
    ret.enroll(text_list, ids=id_list)
    ret.save()
    print("knn - 知识库ID:", zoneID, "bin file saved")


def fileAnalysis(path, zoneID, fileID, is_exist, fileType):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    # 图片与音频类型数据不解析文本内容，由大模型处理
    res = []
    if fileType.lower() in [".jpg", ".png", ".jpeg"]:
        return {"message": "0"}
    if fileType.lower() in [".mp3", ".wav"]:
        data_extractor = DataExtractor(None, asr_model)
        asr = data_extractor.extract_data("audio", path)
        text = convert(asr, "zh-cn")
        res = split_list(text,20)
        print(res)
    else:  # 处理剩余情况
        reader = SimpleDirectoryReader(input_files=[path])
        docs = reader.load_data()
        res = split_list(docs[0].text)
    # sampleDataAddInfo
    for i in range(0, len(res)):
        sdai = {
            "fileID": fileID,
            "dataText": res[i],
            "splitNum": i + 1,
            "createTime": datetime.datetime.now(),
            "modifyTime": None,
        }
        if is_exist:
            conn.update_data(
                "sampleData",
                sdai,
                "fileID=" + str(fileID) + " AND splitNum=" + str(i + 1),
            )
        else:
            conn.insert_data("sampleData", sdai)
    use_knn(zoneID, fileID, fileType)
    print(len(res))


@uploadFiles.post("/newFileAnalysis", summary="文件上传解析")
async def get_file(file: UploadFile, zoneID: int, comment: str = "comment"):
    # print(zoneID, file.filename, file.size)
    kb_path = "/data/personal_wiki/db/uplf/" + str(zoneID)
    if os.path.exists(kb_path) == False:
        os.mkdir(kb_path)
    fi_path = "/data/personal_wiki/db/uplf/" + str(zoneID) + "/" + file.filename
    with open(fi_path, "wb") as f:
        f.write(await file.read())
    uft = {
        "zoneID": zoneID,
        "fileName": file.filename,
        "fileSize": file.size,
        "fileType": os.path.splitext(file.filename)[1],
        "filePosition": fi_path,
        "createTime": datetime.datetime.now(),
        "isDelete": 0,
        "comment": comment,
    }
    is_exist = 0
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    if conn.select_data("uploadFiles", "fileID", 'fileName="' + file.filename + '"'):
        conn.update_data("uploadFiles", uft, 'fileName="' + file.filename + '"')
        is_exist = 1
    else:
        conn.insert_data("uploadFiles", uft)
    select_res = conn.select_data(
        "uploadFiles", "fileID,fileType", 'fileName="' + file.filename + '"'
    )
    fileID = dict(select_res[0])["fileID"]
    fileType = dict(select_res[0])["fileType"]
    fileAnalysis(fi_path, zoneID, fileID, is_exist, fileType)
    return {
        "errorCode": "0",
        "msg": "SUCCESS",
        "requestId": "",
        "result": [{"fileId": fileID, "fileName": file.filename, "status": "0"}],
    }


@uploadFiles.get("/info", summary="查询知识库ID对应的文件信息")
def uploadFilesInfo(zoneID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    result = conn.select_data(
        "uploadFiles", None, f"zoneID='{zoneID}' and isDelete != 1 "
    )
    return result


@uploadFiles.post("/add", summary="新增文件")
def uploadFilesAdd(uploadFilesAddInfo: uploadFilesType):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    uploadFilesAddInfo = uploadFilesAddInfo.dict()
    conn.insert_data("uploadFiles", uploadFilesAddInfo)
    return {"message": 200}


@uploadFiles.delete("/delete", summary="删除文件")
def uploadFilesDelete(fileID: int):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "uploadFiles",
        {"isDelete": "1", "modifyTime": datetime.datetime.now()},
        f"fileID='{fileID}'",
    )
    return {"message": 200}


@uploadFiles.put("/fileComment", summary="更新文件信息备注")
def uploadFilesChangeComment(fileID: int, newComment: str):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "uploadFiles",
        {"comment": newComment, "modifyTime": datetime.datetime.now()},
        f"fileID='{fileID}'",
    )
    return {"message": 200}


@uploadFiles.put("/fileStaus", summary="更新文件状态")
def uploadFilesChangeStatus(fileID: int, newStatus: str):
    conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")
    conn.update_data(
        "uploadFiles",
        {"status": newStatus, "modifyTime": datetime.datetime.now()},
        f"fileID='{fileID}'",
    )
    return {"message": 200}
