import os
import sys
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

#DB호출
loginPath = os.path.join(os.path.dirname(__file__),"DB","1loginInfo.json")
alarmPath = os.path.join(os.path.dirname(__file__),"DB","3worksAlarm.json")
with open(loginPath,'r',encoding="UTF-8") as f:
    login = json.load(f)
works_login = pd.Series(login['works'])

#알람데이터 json파일 저장
def postJson(newalarm:dict) -> None:
    AR = pd.read_json(alarmPath,orient='records',dtype={'Alarm':str})
    AR.drop([0],axis=0,inplace=True)
    add = pd.DataFrame(newalarm,index=[0])
    con = pd.concat([AR,add],ignore_index=True)
    con.to_json(alarmPath,orient='records',force_ascii=False,indent=4)

#분류 데이터 생성
class category:
    #기준 고정값
    def __init__(self):
        self.roomName = ["<AI_MON:PG>","<AI_MON:VAN>","<AI_MON:성공율하락>","<AI_MON:거래감소>","<AI_MON:Error>","<AI_MON:거래급증>"]\

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
    def newAlarm(self,page) -> None:
        for rooms in self.roomName:
            page.find_element(By.XPATH,f'//strong[@title="{rooms}"]').click()
            time.sleep(1)
            soup = BeautifulSoup(page.page_source,'html.parser')
            alarms = soup.find_all('div',class_="msg_lft msg_wrap")
            for div in alarms[-(alarms.__len__()/2):-1]:
                alarmBF = pd.read_json(alarmPath,orient='records',dtype={'Alarm':str,'date':str})
                alarmIndex = alarmBF["Alarm"].tolist()
                alarmText = div.find('div',class_="msg_box").get_text().replace('●','<br>●')
                if alarmText in alarmIndex:
                    pass
                elif '◎' in alarmText:
                    pass
                else:
                    date = alarmText.split("<br>●실시간 상황")[0].split("●알람일시: ")[1]
                    alarmBF.drop([0],axis=0,inplace=True)
                    newAlarm = pd.DataFrame([{'Alarm':alarmText,'date':date}])
                    alarmAF = pd.concat([alarmBF,newAlarm],ignore_index=True)
                    alarmResults = alarmAF.sort_values('date')
                    alarmResults.to_json(alarmPath,orient='records',force_ascii=False,indent=4)

autoAlarm = category()

#구동
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=options)
    driver.get("https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Ftalk.worksmobile.com%2F")
    autoAlarm.getHome(driver)
    try:
        while True:
            autoAlarm.newAlarm(driver)
            time.sleep(0.1)
    except:
        time.sleep(1)
        driver.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    main()