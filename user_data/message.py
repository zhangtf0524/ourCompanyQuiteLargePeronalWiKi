# -*- coding: utf-8 -*-
# @Time    : 2024/3/14  13:10
# @FileName: message.py
# @Software: vsCode
"""
    Description: 用户消息队列
"""


import json
from fastapi import APIRouter
import requests
from db.sqliteOperation import Sqlite3Database
from utils.model_loader import text2vec_model, clip_model
from utils.text_retriever import TextRetriever
from utils.image_retriever import ImageRetriever

message = APIRouter(prefix="/message", tags=["对话界面"])
conn = Sqlite3Database("/data/personal_wiki/db/personal_wiki.db")


@message.post("/chat", summary="消息对话")
async def chat(data: dict):  # zoneIDs: list, history: list,
    question = data["question"]
    zoneIDs = data["zoneIDs"]
    history = data["history"]

    all_res = set()

    for zoneID in zoneIDs:
        knn_file_path = f"/data/personal_wiki/assets/{zoneID}.bin"
        ret = TextRetriever(knn_file_path, text2vec_model)
        # 取出来sampleID
        resIDs = ret.retrieve(question)
        for resID in resIDs:
            res = conn.select_data("sampleData", "dataText", f'sampleID="{resID}"')
            all_res.add(dict(res[0])["dataText"])

    api_url = "http://127.0.0.1:9527/api"
    instruction = "你是一个擅长总结我给出的参考信息，作出长文回答的助手。"
    # knn -> sample id 查sql拿到text -> text 装载入text
    references = list(all_res)
    ref = "\n".join(references)
    prompt = f"{question} \n 请参考以下内容作答：\n{ref}"
    data = {"query": instruction + prompt, "history": history}
    r = requests.post(api_url, json=data)
    reply_d = json.loads(r.text)
    reply = reply_d.get("reply", "")
    
    # 图片处理
    img_res=[]
    for zoneID in zoneIDs: 
        img_select = conn.select_data(
            "uploadFiles", "filePosition,fileType,fileName", f'zoneID="{zoneID}" AND fileType in (".jpg", ".png", ".jpeg")'
        )
        
        for i in range(0,len(img_select)):
            img_res.append(img_select[i])
    # print(img_res)
    if len(img_res)==0:
        return {
        "reply": reply,
        "source": [],
    }
    img_list_filePosition = []
    for i in range(0, len(img_res)):
        img_list_filePosition.append(dict(img_res[i])["filePosition"])
    img_ret = ImageRetriever(img_list_filePosition, clip_model)
    res_img_ret = img_ret.retrieve(question)
    print(res_img_ret)
    source = []
    for i in range(0, len(res_img_ret)):
        res = conn.select_data(
            "uploadFiles",
            "fileType,fileName,zoneID",
            f'filePosition="{res_img_ret[i]}"',
        )
        filetype = dict(res[0])["fileType"]
        name = dict(res[0])["fileName"]
        zone_ID = dict(res[0])["zoneID"]
        
        source.append(
            {
                'type': filetype,
                'name': name,
                'url': f'http://116.63.189.245:8000/static/{zone_ID}/{name}',
            }
        )
    return {
        "reply": reply,
        "source": source,
    }
