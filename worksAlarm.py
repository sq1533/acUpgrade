import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#크롬 옵션설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument("--disable-javascript")
options.add_argument('--disable-extensions')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
from bs4 import BeautifulSoup
import pandas as pd
import json
#로그인 정보 호출
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json','r',encoding="UTF-8") as f:
    login = json.load(f)
works_login = pd.Series(login['works'])

#크롬 드라이버 실행
url = "https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Ftalk.worksmobile.com%2F"
driver.get(url)
driver.implicitly_wait(1)
#로그인 정보입력(아이디)
id_box = driver.find_element(By.XPATH,'//input[@id="user_id"]')
login_button_1 = driver.find_element(By.XPATH,'//button[@id="loginStart"]')
ActionChains(driver)
id = works_login['id']
ActionChains(driver).send_keys_to_element(id_box, '{}'.format(id)).click(login_button_1).perform()
time.sleep(1)
#로그인 정보입력(비밀번호)
password_box = driver.find_element(By.XPATH,'//input[@id="user_pwd"]')
login_button_2 = driver.find_element(By.XPATH,'//button[@id="loginBtn"]')
password = works_login['pw']
ActionChains(driver).send_keys_to_element(password_box, '{}'.format(password)).click(login_button_2).perform()
time.sleep(1)

#알람제외 대상자
exce = ['정상화','개시가','◎','처리 정상','정상처리','대기/장애','활동/정상']
#AI_MON simple 알람 타켓
target_simple = [':거래없음',':거래감소',':거래(성공건)없음',':거래급증',':거래(오류)급증',':성공율 하락',':비정상환불',':비정상취소']
#AI_MON error 알람 타켓
target_error = [':동일오류',':오류발생']
#알람방 타켓
a_room = ["26143386","26143422","26143419","82166397","26143441","108290282","108290470","26143427"]

#알람데이터 json파일 저장
def re(x):
    alarmJson = x.to_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient='records',force_ascii=False,indent=4)
    new_alarm = driver.find_element(By.CLASS_NAME,'chat_list').find_element(By.CLASS_NAME,'new')
    new_alarm.click()
    driver.refresh()
    return alarmJson
#알람데이터 크롤링
def alarmcheck():
    AR = pd.read_json('C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json',orient='records',dtype={'Alarm':str,'mid':str})
    r = len(AR)
    if r > 10:
        AR.drop([0],axis=0,inplace=True)
        Alarm = AR
    else:
        Alarm = AR
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    check = {"data-key":a_room, "class":"item_chat"}
    if soup.find('li',check).find(class_='new') != None:
        A_li = soup.find('li',check).find(class_='new').find_parent('li')
        AI_alarm = A_li.find('dd').get_text()
        AI_alarm = AI_alarm.replace('●','<br>●')
        #재외처리 알람
        if any(i in AI_alarm for i in exce):
            pass
        #특수 알람
        elif '자동취소응답오류' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["자동취소응답오류"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '기관 재판매 PG 정산 정보 없음' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["재판매 정산 정보 없음"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'vavsreceipt' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["vavsreceipt"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '현금영수증' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["현금영수증"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'autocancel' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["autocancel"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '거래없음[' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["VAN_거래없음"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '은행 잔액 부족' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["가상 재판매 모계좌 잔액부족"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '응답지연' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["응답지연"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '응답 지연' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["응답지연"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '/미처리' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["미처리"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '(50)장애발생' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["저축은행 가상"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'VDBE' in AI_alarm:
            a = {
                "Alarm":[AI_alarm],
                "mid":["VDBE"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif '큐확인요망' in AI_alarm:
            al = AI_alarm.split(' ')
            F_code = al[1]
            a = {
                "Alarm":[AI_alarm],
                "mid":[F_code]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'VAN 20' in AI_alarm:
            al = AI_alarm.split(' ')
            V_code = al[3]
            a = {
                "Alarm":[AI_alarm],
                "mid":[V_code]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'CONNECT' in AI_alarm:
            VV_code_1 = AI_alarm.replace('(주)','').replace('(지역페이)','').replace('(지정계좌)','').replace('(쇼핑)','')
            VV_code_2 = VV_code_1.split('(',1)
            VV_code_3 = VV_code_2[1].split(')',1)
            VV_code = VV_code_3[0]
            a = {
                "Alarm":[AI_alarm],
                "mid":[VV_code]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif 'TIME' in AI_alarm:
            VV_code_1 = AI_alarm.replace('(주)','').replace('(지역페이)','').replace('(지정계좌)','').replace('(쇼핑)','')
            VV_code_2 = VV_code_1.split('(',1)
            VV_code_3 = VV_code_2[1].split(')',1)
            VV_code = VV_code_3[0]
            a = {
                "Alarm":[AI_alarm],
                "mid":[VV_code]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        #AI_MON 알람
        elif any(i in AI_alarm for i in target_simple):
            MID_1 = AI_alarm.split('가맹점:')
            MID_2 = MID_1[1].split('[',1)
            MID_3 = MID_2[1].split(']',1)
            MID = MID_3[0]
            a = {
                "Alarm":[AI_alarm],
                "mid":[MID]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        elif any(i in AI_alarm for i in target_error):
            AI = AI_alarm.replace(' ','')
            MID_1 = AI.split('오류코드:')
            MID_2 = MID_1[1].split('(',1)
            code = str(MID_2[0])
            a = {
                "Alarm":[AI_alarm],
                "mid":[code]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
        else:
            a = {
                "Alarm":[AI_alarm],
                "mid":["확인필요"]
                }
            ad = pd.DataFrame(a,index=[0])
            con = pd.concat([Alarm,ad],ignore_index=True)
            re(con)
    else:
        pass
    return Alarm
while True:
    alarmcheck()
    time.sleep(0.1)