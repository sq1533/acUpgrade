from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json','r',encoding="UTF-8") as f:
    login = json.load(f)
works_login = pd.Series(login['works'])
#알람제외 대상자
EXCEPT = ['정상화','개시가','◎','처리 정상','정상처리','대기/장애','활동/정상']
#AI_MON simple 알람 타켓
target_simple = [':거래없음',':거래감소',':거래(성공건)없음',':거래급증',':거래(오류)급증',':성공율 하락',':비정상환불',':비정상취소']
#AI_MON error 알람 타켓
target_error = [':동일오류',':오류발생']
#알람방 타켓
a_room = ["26143386","26143422","26143419","82166397","26143441","108290282","108290470","26143427"]
#알람데이터 json파일 저장
def postJson(x):
    alarmJson = x.to_json("C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json",orient='records',force_ascii=False,indent=4)
    return alarmJson
#페이지 로그인
def getHome(page):
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
def alarmCheck(page):
    soup = BeautifulSoup(page.page_source,'html.parser')
    check = {"data-key":a_room, "class":"item_chat"}
    if soup.find('li',check).find(class_='new') != None:
        AR = pd.read_json('C:\\Users\\USER\\ve_1\\DB\\1worksAlarm.json',orient='records',dtype={'Alarm':str,'mid':str})
        A_li = soup.find('li',check).find(class_='new').find_parent('li')
        AI_alarm = A_li.find('dd').get_text().replace('●','<br>●')
        if any(i in AI_alarm for i in EXCEPT):pass
        elif '자동취소응답오류' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["자동취소응답오류"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '기관 재판매 PG 정산 정보 없음' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["재판매 정산 정보 없음"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'vavsreceipt' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["vavsreceipt"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '현금영수증' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["현금영수증"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'autocancel' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["autocancel"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '거래없음[' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["VAN_거래없음"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '은행 잔액 부족' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["가상 재판매 모계좌 잔액부족"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '응답지연' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["응답지연"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '응답 지연' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["응답지연"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '/미처리' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["미처리"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '(50)장애발생' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["저축은행 가상"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'VDBE' in AI_alarm:
            a = {"Alarm":[AI_alarm],"mid":["VDBE"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif '큐확인요망' in AI_alarm:
            al = AI_alarm.split(' ')
            F_code = al[1]
            a = {"Alarm":[AI_alarm],"mid":[F_code]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'VAN 20' in AI_alarm:
            al = AI_alarm.split(' ')
            V_code = al[3]
            a = {"Alarm":[AI_alarm],"mid":[V_code]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'CONNECT' in AI_alarm:
            VV_code_1 = AI_alarm.replace('(주)','').replace('(지역페이)','').replace('(지정계좌)','').replace('(쇼핑)','').replace('(공영주차)','')
            VV_code_2 = VV_code_1.split('(',1)
            VV_code_3 = VV_code_2[1].split(')',1)
            VV_code = VV_code_3[0]
            a = {"Alarm":[AI_alarm],"mid":[VV_code]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif 'TIME' in AI_alarm:
            VV_code_1 = AI_alarm.replace('(주)','').replace('(지역페이)','').replace('(지정계좌)','').replace('(쇼핑)','').replace('(공영주차)','')
            VV_code_2 = VV_code_1.split('(',1)
            VV_code_3 = VV_code_2[1].split(')',1)
            VV_code = VV_code_3[0]
            a = {"Alarm":[AI_alarm],"mid":[VV_code]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        #AI_MON 알람
        elif any(i in AI_alarm for i in target_simple):
            MID_1 = AI_alarm.split('가맹점:')
            MID_2 = MID_1[1].split('[',1)
            MID_3 = MID_2[1].split(']',1)
            MID = MID_3[0]
            a = {"Alarm":[AI_alarm],"mid":[MID]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        elif any(i in AI_alarm for i in target_error):
            AI = AI_alarm.replace(' ','')
            MID_1 = AI.split('오류코드:')
            MID_2 = MID_1[1].split('(',1)
            code = str(MID_2[0])
            a = {"Alarm":[AI_alarm],"mid":[code]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        else:
            a = {"Alarm":[AI_alarm],"mid":["확인필요"]}
            add = pd.DataFrame(a,index=[0])
            AR.drop([0],axis=0,inplace=True)
            con = pd.concat([AR,add],ignore_index=True)
            postJson(con)
        new_alarm = page.find_element(By.CLASS_NAME,'chat_list').find_element(By.CLASS_NAME,'new')
        new_alarm.click()
        page.refresh()
        time.sleep(1.5)
    else:pass
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)
    driver.get("https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Ftalk.worksmobile.com%2F")
    try:
        getHome(driver)
        while True:
            alarmCheck(driver)
            time.sleep(0.1)
    except:
        driver.quit()
        time.sleep(5)
        main()
if __name__ == "__main__":main()