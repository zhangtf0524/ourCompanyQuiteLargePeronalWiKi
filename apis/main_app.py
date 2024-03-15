import sys

sys.path.append("/data/personal_wiki/")

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from db.user import user as user_router
from db.wikiZone import wikiZone as wikiZone_router
from db.sampleData import sampleData as sampleData_router
from db.uploadFiles import uploadFiles as uploadFiles_router
from user_data.message import message as message_router
import utils.model_loader
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user_router)
app.include_router(wikiZone_router)
app.include_router(sampleData_router)
app.include_router(uploadFiles_router)
app.include_router(message_router)

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins=["*"],
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=False,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="/data/personal_wiki/db/uplf"))

@app.get("/", tags=["主程序"])
async def main_entrance():
    return {"main": "this is main"}


if __name__ == "__main__":
    uvicorn.run(
        app="main_app:app",
        host="0.0.0.0",
        port=8000,
        use_colors=True,
    )

