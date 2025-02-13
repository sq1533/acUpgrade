import os
import sys
import subprocess
import json
import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

#재시작 프로토콜
def restart_script():
    driver.quit()
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()

#로그인 정보 호출
loginPath = os.path.join(os.path.dirname(__file__),"DB","1loginInfo.json")
with open(loginPath,'r',encoding="UTF-8") as f:
    login = json.load(f)
works_login = pd.Series(login['works'])

#분류 데이터 생성
class category:
    def __init__(self):
        self.roomName = ["<AI_MON:PG>","<AI_MON:VAN>","<AI_MON:성공율하락>","<AI_MON:거래감소>","<AI_MON:Error>","<AI_MON:거래급증>"]

    #페이지 로그인
    def getHome(self,page) -> None:
        #로그인 정보입력(아이디)
        id_box = page.find_element(By.XPATH,'//input[@id="user_id"]')
        login_button_1 = page.find_element(By.XPATH,'//button[@id="loginStart"]')
        ActionChains(page)
        id = works_login['id']
        ActionChains(page).send_keys_to_element(id_box, '{}'.format(id)).click(login_button_1).perform()
        time.sleep(1)
        #로그인 정보입력(비밀번호)
        password_box = page.find_element(By.XPATH,'//input[@id="user_pwd"]')
        login_button_2 = page.find_element(By.XPATH,'//button[@id="loginBtn"]')
        password = works_login['pw']
        ActionChains(page).send_keys_to_element(password_box, '{}'.format(password)).click(login_button_2).perform()
        time.sleep(1)

    #알람데이터 크롤링
    def newAlarm(self,page,path) -> None:
        blink = []
        for rooms in self.roomName:
            page.find_element(By.XPATH,f'//strong[@title="{rooms}"]').click()
            time.sleep(2)
            soup = BeautifulSoup(page.page_source,'html.parser')
            alarms = soup.find_all('div',class_="msg_area")
            lens = alarms.__len__()
            for div in range(lens-1,int(lens/2),-1):
                alarmText = alarms[div].find('div',class_="msg_box").getText().replace('●','<br>●')
                if '◎' in alarmText:
                    pass
                else:
                    date = alarmText.split("<br>●실시간 상황")[0].split("●알람일시: ")[1]
                    blink.append([alarmText,date,"nonCheck"])
            alarmBF = pd.read_json(path,orient='records',dtype={'Alarm':str,'date':str,'check':str})
            validateData1 = set([i[0] for i in blink])
            validateData2 = set(alarmBF['Alarm'].tolist())
            unique = list(validateData1 - validateData2)
            if unique:
                newdata = [alarm for alarm in blink if alarm[0] in unique]
                new = pd.DataFrame(data=newdata,columns=["Alarm","date","check"])
                alarmAF = pd.concat([alarmBF,new],ignore_index=True)
                alarmResults = alarmAF.sort_values(by=['check','date'],ascending=[True, False]).groupby('check').head(len(alarmAF)).reset_index(drop=True)
                alarmResults.to_json(path,orient='records',force_ascii=False,indent=4)
            else:
                pass

#class 정의
autoAlarm = category()
#브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options=options)
driver.get("https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Ftalk.worksmobile.com")
autoAlarm.getHome(driver)
max_runtime = 7200
start_time = time.time()

#구동
def main():
    now = datetime.date.today()
    todayAlarmPath = os.path.join(os.path.dirname(__file__),"Alarm",f"worksAlarm_{now.strftime("%y%m%d")}.json")
    if os.path.exists(todayAlarmPath):
        try:
            print(int(time.time()-start_time))
            autoAlarm.newAlarm(driver,todayAlarmPath)
            if (time.time()-start_time) >= max_runtime:
                time.sleep(1)
                restart_script()
            else:
                pass
        except Exception as ec:
            print(ec)
            driver.quit()
            time.sleep(1)
            restart_script()
    else:
        yesterday = now - datetime.timedelta(days=1)
        dropData = now - datetime.timedelta(days=2)
        yesterdayAlarmPath = os.path.join(os.path.dirname(__file__),"Alarm",f"worksAlarm_{yesterday.strftime("%y%m%d")}.json")
        yesterdayData = pd.read_json(yesterdayAlarmPath,orient='records',dtype={'Alarm':str,'date':str,'check':str})
        todayData = yesterdayData[~yesterdayData['date'].str.contains(dropData.strftime("%m%d"),na=False)]
        todayData.to_json(todayAlarmPath,orient='records',force_ascii=False,indent=4)

if __name__ == "__main__":
    while True:
        try:
            main()
            time.sleep(0.1)
        except Exception as e:
            print(e)
            time.sleep(2)