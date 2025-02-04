import os
import pandas as pd
import re
import datetime
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import database

now = datetime.date.today()
alarmPath = os.path.join(os.path.dirname(__file__),"DB",f"3worksAlarm_{now.strftime("%m%d")}.json")
midInfoPath = os.path.join(os.path.dirname(__file__),"DB","2midInfo.json")

#AI_MON simple 알람 타켓
target_simple = [':거래없음',':거래감소',':거래(성공건)없음',':거래급증',':거래(오류)급증',':성공율 하락',':비정상환불',':비정상취소']
#AI_MON error 알람 타켓
target_error = [':동일오류',':오류발생']

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
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"data":str})
    links = urls_to_links(alarm.iloc[-number]['Alarm'])
    return HTMLResponse(content=links)

#alarm 정보
@app.get("/alarmInfo_{number}")
def alarm_info(number:int):
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"data":str}).iloc[-number]["Alarm"]
    if any(i in alarm for i in target_simple):
        MID_1 = alarm.split('가맹점:')
        MID_2 = MID_1[1].split('[',1)
        MID_3 = MID_2[1].split(']',1)
        MID = MID_3[0]
        alarmAF = {"Alarm":alarm,"mid":MID}
    elif any(i in alarm for i in target_error):
        AI = alarm.replace(' ','')
        MID_1 = AI.split('오류코드:')
        MID_2 = MID_1[1].split('(',1)
        code = str(MID_2[0])
        alarmAF = {"Alarm":alarm,"mid":code}
    else:
        alarmAF = {"Alarm":alarm,"mid":"None"}
    info = pd.read_json(midInfoPath,orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarmAF['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarmAF['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarmAF['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)

#alarm 담당자
@app.get("/alarmChar_{number}")
def alarm_chcr(number:int):
    alarm = pd.read_json(alarmPath,orient="records",dtype={"Alarm":str,"data":str}).iloc[-number]["Alarm"]
    if any(i in alarm for i in target_simple):
        MID_1 = alarm.split('가맹점:')
        MID_2 = MID_1[1].split('[',1)
        MID_3 = MID_2[1].split(']',1)
        MID = MID_3[0]
        alarmAF = {"Alarm":alarm,"mid":MID}
    elif any(i in alarm for i in target_error):
        AI = alarm.replace(' ','')
        MID_1 = AI.split('오류코드:')
        MID_2 = MID_1[1].split('(',1)
        code = str(MID_2[0])
        alarmAF = {"Alarm":alarm,"mid":code}
    else:
        alarmAF = {"Alarm":alarm,"mid":"None"}
    info = pd.read_json(midInfoPath,orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarmAF['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarmAF['mid']])]['char'].reset_index(drop=True)[0])
    else:
        midInfo = "none"
    return HTMLResponse(content=midInfo)

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