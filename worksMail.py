import time
import json
import pandas as pd

def ezMail(id:str,pw:str):
    #크롬 드라이버 옵션 설정
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    #크롬 드라이버 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=chrome_options)
    #크롬 드라이버 실행
    url = "https://auth.worksmobile.com/login/login?accessUrl=https%3A%2F%2Fmail.worksmobile.com%2F"
    driver.get(url)
    driver.implicitly_wait(1)
    #로그인 정보입력(아이디)
    id_box = driver.find_element(By.XPATH,'//input[@id="user_id"]')
    login_button_1 = driver.find_element(By.XPATH,'//button[@id="loginStart"]')
    ActionChains(driver)
    ActionChains(driver).send_keys_to_element(id_box, '{}'.format(id)).click(login_button_1).perform()
    time.sleep(1)
    #로그인 정보입력(비밀번호)
    password_box = driver.find_element(By.XPATH,'//input[@id="user_pwd"]')
    login_button_2 = driver.find_element(By.XPATH,'//button[@id="loginBtn"]')
    ActionChains(driver).send_keys_to_element(password_box, '{}'.format(pw)).click(login_button_2).perform()
    time.sleep(1)
    #인증번호 전송
    passingMail = driver.find_element(By.XPATH,'//a[@id="privateEmailButton"]')
    ActionChains(driver).click(passingMail).perform()
    time.sleep(5)
    while True:
        mail = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-3mailAccess.json",orient='records',dtype={"passnumber":str,"addr":str,"subaddr":str,"title":str,"main":str})
        #인증번호 검증
        if not(mail['passnumber'].tolist()[-1].isdigit()):
            time.sleep(0.5)
            pass
        else:
            #인증 진행
            passingN = driver.find_element(By.XPATH,'//input[@id="number1"]')
            passingnumber = mail['passnumber'].tolist()[-1]
            ActionChains(driver).click(passingN).send_keys('{}'.format(passingnumber)).perform()
            time.sleep(1)
            #메일전송 페이지 전환
            driver.get('https://mail.worksmobile.com/#/compose?orderType=new')
            time.sleep(2)
            driver.maximize_window()
            time.sleep(1)
            address = driver.find_element(By.XPATH,'//input[@aria-label="받는사람"]')#수신자 입력창
            subaddress = driver.find_element(By.XPATH,'//input[@aria-label="참조"]')#참조 입력창
            mailtitle = driver.find_element(By.XPATH,'//input[@aria-label="제목"]')#제목 입력창
            mailmain = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[3]/div[2]/div/fieldset/div/div/div/div[3]')#내용 입력창
            send_button = driver.find_element(By.XPATH,'//button[@data-hotkey="sendKey"]')#전송 버튼
            send_each = driver.find_element(By.XPATH,'//input[@name="sendSeparately"]')#개인별 체크박스
            #메일내용 입력
            mmain = mail['main'].tolist()[-1]
            ActionChains(driver).click(mailmain).send_keys(Keys.PAGE_UP).send_keys('{}'.format(mmain)).perform()
            time.sleep(1)
            #메일제목 입력
            mtitle = mail['title'].tolist()[-1]
            ActionChains(driver).click(mailtitle).send_keys_to_element(mailtitle,'{}'.format(mtitle)).perform()
            time.sleep(1)
            #참조 입력
            subaddrs = mail['subaddr'].tolist()[-1]
            ActionChains(driver).send_keys_to_element(subaddress, '{}'.format(subaddrs)).perform()
            time.sleep(1)
            #수신자 입력
            addrs = mail['addr'].tolist()[-1]
            ActionChains(driver).send_keys_to_element(address, '{}'.format(addrs)).perform()
            time.sleep(1)
            #개인별 전송 클릭
            ActionChains(driver).click(send_each).perform()
            time.sleep(1)
            #전송 클릭_1
            ActionChains(driver).click(send_button).perform()
            time.sleep(5)
            """
            #전송 클릭_2
            send_button = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div/h3/div/button[1]')
            ActionChains(driver).click(send_button).perform()
            time.sleep(5)
            """
            driver.quit()
            mailReset = {
                "passnumber":"test",
                "addr":"test_a",
                "subaddr":"test_s",
                "title":"test_t",
                "main":"test_m"
                }
            pd.DataFrame(mailReset,index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-3mailAccess.json',orient='records',force_ascii=False,indent=4)
            time.sleep(1)
            break

if __name__ == "__main__":
    while True:
        #로그인 및 시작 정보 확인
        with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json','r',encoding='utf-8') as f:
            loginInfo = json.load(f)
        enMail = pd.Series(loginInfo["enMail"])
        coochip = pd.Series(loginInfo["coochip"])
        startPoint = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json",orient='records')
        if startPoint['coochip'].tolist()[0] == 'start':
            ezMail(coochip['id'],coochip['pw'])
            pd.DataFrame({"coochip":"end","enMail":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        elif startPoint['enMail'].tolist()[0] == 'start':
            ezMail(enMail['id'],enMail['pw'])
            pd.DataFrame({"coochip":"end","enMail":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        else:
            time.sleep(1)
            pass