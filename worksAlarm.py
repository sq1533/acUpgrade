import os
import sys
import json
import pandas as pd
import time
import re
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
    AR = pd.read_json(alarmPath,orient='records',dtype={'Alarm':str,'mid':str})
    AR.drop([0],axis=0,inplace=True)
    add = pd.DataFrame(newalarm,index=[0])
    con = pd.concat([AR,add],ignore_index=True)
    con.to_json(alarmPath,orient='records',force_ascii=False,indent=4)

#분류 데이터 생성
class category:
    def __init__(self):
        #알람제외 대상자
        self.EXCEPT = ['정상화','개시가','◎','처리 정상','정상처리','대기/장애','활동/정상']
        #AI_MON simple 알람 타켓
        self.target_simple = [':거래없음',':거래감소',':거래(성공건)없음',':거래급증',':거래(오류)급증',':성공율 하락',':비정상환불',':비정상취소']
        #AI_MON error 알람 타켓
        self.target_error = [':동일오류',':오류발생']
        #알람방 타켓
        self.a_room = ["26143386","26143422","26143419","82166397","26143441","108290282","108290470","26143427"]

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
        soup = BeautifulSoup(page.page_source,'html.parser')
        check = {"data-key":self.a_room, "class":"item_chat"}
        new_alarm = soup.find('li',check).find(class_='new')
        if new_alarm == None:
            pass
        else:
            new_alarm = new_alarm.find_parent('li').find('dd').get_text().replace('●','<br>●')
            category.ALARM(self,new_alarm)
            page.find_element(By.CLASS_NAME,'chat_list').find_element(By.CLASS_NAME,'new').click()
            page.find_elements(By.CLASS_NAME,'item_chat')[8].find_element(By.CLASS_NAME,'chat_cont_area').click()

    #알람 분류
    def ALARM(self,alarm) -> None:
            if any(i in alarm for i in self.EXCEPT):
                pass
            elif '자동정산 요청 거래 없음' in alarm:
                a = {"Alarm":[alarm],"mid":["자동정산 요청 거래 없음"]}
                postJson(a)
            elif 'prcchk' in alarm:
                a = {"Alarm":[alarm],"mid":["prcchk"]}
                postJson(a)
            elif '자동취소응답오류' in alarm:
                a = {"Alarm":[alarm],"mid":["자동취소응답오류"]}
                postJson(a)
            elif '정산 정보 없음' in alarm:
                a = {"Alarm":[alarm],"mid":["정산 정보 없음"]}
                postJson(a)
            elif 'vavsreceipt' in alarm:
                a = {"Alarm":[alarm],"mid":["vavsreceipt"]}
                postJson(a)
            elif '현금영수증' in alarm:
                a = {"Alarm":[alarm],"mid":["현금영수증"]}
                postJson(a)
            elif 'autocancel' in alarm:
                a = {"Alarm":[alarm],"mid":["autocancel"]}
                postJson(a)
            elif '거래없음[' in alarm:
                a = {"Alarm":[alarm],"mid":["VAN거래없음"]}
                postJson(a)
            elif '은행 잔액 부족' in alarm:
                a = {"Alarm":[alarm],"mid":["은행 잔액 부족"]}
                postJson(a)
            elif '응답지연' in alarm or '응답 지연' in alarm:
                a = {"Alarm":[alarm],"mid":["응답지연"]}
                postJson(a)
            elif '/미처리' in alarm:
                a = {"Alarm":[alarm],"mid":["미처리"]}
                postJson(a)
            elif ')장애발생' in alarm:
                a = {"Alarm":[alarm],"mid":["VAN가상장애"]}
                postJson(a)
            elif 'VDBE' in alarm:
                a = {"Alarm":[alarm],"mid":["VDBE"]}
                postJson(a)
            elif '큐확인요망' in alarm:
                preAlarm = alarm.split(' ')
                Firm_code = preAlarm[1]
                a = {"Alarm":[alarm],"mid":[Firm_code]}
                postJson(a)
            elif 'VAN 20' in alarm:
                preAlarm = alarm.split(' ')
                vs_code = preAlarm[3]
                a = {"Alarm":[alarm],"mid":[vs_code]}
                postJson(a)
            elif 'CONNECT' in alarm:
                preAlarm = re.search(r'\((\d+)\)',alarm)
                vs_code = preAlarm.group(1)
                a = {"Alarm":[alarm],"mid":[vs_code]}
                postJson(a)
            elif 'TIME' in alarm:
                preAlarm = re.search(r'\((\d+)\)',alarm)
                vs_code = preAlarm.group(1)
                a = {"Alarm":[alarm],"mid":[vs_code]}
                postJson(a)
            #AI_MON 알람
            elif any(i in alarm for i in self.target_simple):
                MID_1 = alarm.split('가맹점:')
                MID_2 = MID_1[1].split('[',1)
                MID_3 = MID_2[1].split(']',1)
                MID = MID_3[0]
                a = {"Alarm":[alarm],"mid":[MID]}
                postJson(a)
            elif any(i in alarm for i in self.target_error):
                AI = alarm.replace(' ','')
                MID_1 = AI.split('오류코드:')
                MID_2 = MID_1[1].split('(',1)
                code = str(MID_2[0])
                a = {"Alarm":[alarm],"mid":[code]}
                postJson(a)
            else:
                a = {"Alarm":[alarm],"mid":["확인필요"]}
                postJson(a)

autoAlarm = category()

#구동
def main():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Ftalk.worksmobile.com%2F")
        autoAlarm.getHome(driver)
        while True:
            autoAlarm.newAlarm(driver)
            time.sleep(0.1)
    except:
        time.sleep(1)
        driver.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    main()