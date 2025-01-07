import os
import pandas as pd
import re
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import database

midInfoPath = os.path.join(os.path.dirname(__file__),"DB","2midInfo.json")
alarmPath = os.path.join(os.path.dirname(__file__),"DB","3worksAlarm.json")

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"templates"))

#URL 정제
def urls_to_links(text):
    url = r'(https?://[^\s<]+)'
    return re.sub(url,r'<a href="\1" target="_blank">\1</a>',text)

#homePage
@app.get("/home",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

#alarm
@app.get("/alarm_{number}")
def alarm_1(number:int):
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-number]['Alarm'])
    return HTMLResponse(content=links)

#alarm 정보
@app.get("/alarmInfo_{number}")
def alarm_info(number:int):
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json(midInfoPath,orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-number]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-number]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-number]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)

#alarm 담당자
@app.get("/alarmChar_{number}")
def alarm_chcr(number:int):
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json(midInfoPath,orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-number]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-number]['mid']])]['char'].reset_index(drop=True)[0]
    else:
        midChar = "none"
    return HTMLResponse(content=midChar)

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
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8501)