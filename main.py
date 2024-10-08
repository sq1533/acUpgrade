from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import re
import database
app = FastAPI()
#현재 파일의 디렉토리 경로를 가져옵니다.
templates = Jinja2Templates(directory="templates")
#homePage
@app.get("/home",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})
#URL 정제
def urls_to_links(text):
    url = r'(https?://[^\s<]+)'
    return re.sub(url,r'<a href="\1" target="_blank">\1</a>',text)
#alarm 1번
@app.get("/alarm_1")
def alarm_1():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-1]['Alarm'])
    return HTMLResponse(content=links)
@app.get("/alarm_1_info")
def alarm_1_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-1]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-1]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-1]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)
@app.get("/alarm_1_char")
def alarm_1_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-1]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-1]['mid']])]['char'].reset_index(drop=True)[0]
    else:
        midChar = "none"
    return HTMLResponse(content=midChar)
#alarm 2번
@app.get("/alarm_2")
def alarm_2():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-2]['Alarm'])
    return HTMLResponse(content=links)
@app.get("/alarm_2_info")
def alarm_2_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-2]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-2]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-2]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)
@app.get("/alarm_2_char")
def alarm_2_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-2]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-2]['mid']])]['char'].reset_index(drop=True)[0]
    else:
        midChar = "none"
    return HTMLResponse(content=midChar)
#alarm 3번
@app.get("/alarm_3")
def alarm_3():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-3]['Alarm'])
    return HTMLResponse(content=links)
@app.get("/alarm_3_info")
def alarm_3_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-3]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-3]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-3]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)
@app.get("/alarm_3_char")
def alarm_3_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-3]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-3]['mid']])]['char'].reset_index(drop=True)[0]
    else:
        midChar = "none"
    return HTMLResponse(content=midChar)
#alarm 4번
@app.get("/alarm_4")
def alarm_4():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-4]['Alarm'])
    return HTMLResponse(content=links)
@app.get("/alarm_4_info")
def alarm_4_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-4]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-4]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-4]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)
@app.get("/alarm_4_char")
def alarm_4_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-4]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-4]['mid']])]['char'].reset_index(drop=True)[0]
    else:
        midChar = "none"
    return HTMLResponse(content=midChar)
#alarm 5번
@app.get("/alarm_5")
def alarm_5():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    links = urls_to_links(alarm.iloc[-5]['Alarm'])
    return HTMLResponse(content=links)
@app.get("/alarm_5_info")
def alarm_5_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-5]['mid'] in midList:
        midInfo = urls_to_links(info[info['mid'].isin([alarm.iloc[-5]['mid']])]['info'].reset_index(drop=True)[0])
    else:
        midInfo = str(f"{alarm.iloc[-5]['mid']} DB생성 필요")
    return HTMLResponse(content=midInfo)
@app.get("/alarm_5_char")
def alarm_5_info():
    alarm = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient="records",dtype={"Alarm":str,"mid":str,"URL":str})
    info = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\2midInfo.json",orient="records",dtype={"mid":str,"info":str,"char":str})
    midList = info['mid'].tolist()
    if alarm.iloc[-5]['mid'] in midList:
        midChar = info[info['mid'].isin([alarm.iloc[-5]['mid']])]['char'].reset_index(drop=True)[0]
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
    uvicorn.run(app,host="0.0.0.0",port=8000)