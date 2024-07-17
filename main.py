import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import database

app = FastAPI()

# 현재 파일의 디렉토리 경로를 가져옵니다.
templates = Jinja2Templates(directory="templates")
#데이터 설정
class mk(BaseModel):
    mid : str
    info : str
    char : str
class mid(BaseModel):
    mid : str
class mail(BaseModel):
    passnumber : str
    addr : str
    subaddr : str
    title : str
    main : str
#homePage
@app.get("/home",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})
#생성
@app.post("/mk_info")
async def create(response: mk):
    database.cre(dict(response))
#수정
@app.put("/mk_info")
async def change(response: mk):
    database.put(dict(response))
#삭제
@app.post("/mk_info_d")
async def delete(response: mid):
    database.delete(dict(response))
#메일전송
@app.post("/email")
async def sendMail(response: mail):
    database.mail(dict(response))

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)