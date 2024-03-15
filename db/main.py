import uvicorn
import http
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI
from user import user
from wikiZone import wikiZone
from uploadFiles import uploadFiles
from sampleData import sampleData
from sqliteOperation import Sqlite3Database


app = FastAPI()
app.include_router(user,prefix="/user",tags=["用户"])
app.include_router(wikiZone,prefix="/wikiZone",tags=["知识库"])
app.include_router(uploadFiles,prefix="/uploadFiles",tags=["文件库"])
app.include_router(sampleData,prefix="/sampleData",tags=["样本库"])


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"message": str(e)},
    )


@app.get("/",tags=["HOME"],summary="让我看看")
async def root():
    return {"message":"我们公司还蛮大的"}


if __name__ == '__main__' :
    uvicorn.run("main:app", port=8000, reload=True)

