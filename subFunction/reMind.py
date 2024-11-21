import requests
import json
import pandas as pd
import time
from datetime import datetime
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json', 'r', encoding='utf-8') as f:
    login_info = json.load(f)
bot_info = pd.Series(login_info['nFaxbot'])
bot_HC = pd.Series(login_info['nFaxbot_hc'])
restDay = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\8restDay.json",orient="index")
today = datetime.today()
toMonth = restDay.loc[today.month].dropna().tolist()
#공휴일 리마인드 발송 제외
if today.day not in toMonth:
    if datetime.now().strftime("%H:%M") == "11:00":
        read = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\6-2reMind.json",orient='records',dtype={'date':str,'bank':str,'info':str,'signUp':str})
        for i in range(1,len(read.index.tolist())):
            sendText = f"Fax수신일자 : {read["date"][i]}/n원천사 : {read["bank"][i]}/n팩스정보{read["info"][i]}/n민원등록 여부 : {read["signUp"][i]}"
            requests.get(f"https://api.telegram.org/bot{bot_info['token']}/sendMessage?chat_id={bot_info['chatId']}&text={sendText}")
            time.sleep(1)
        #발송 후 데이터 리셋
        pd.DataFrame(data={"date":"test","bank":"test","info":"test","signUp":"test"},index=[0]).to_json("C:\\Users\\USER\\ve_1\\DB\\6-2reMind.json",orient='records',force_ascii=False,indent=4)
        requests.get(f"https://api.telegram.org/bot{bot_HC['token']}/sendMessage?chat_id={bot_HC['chatId']}&text=리마인드 전송 및 리셋")
        time.sleep(60)
    else:
        time.sleep(30)
        pass
else:
    time.sleep(36000)
    pass