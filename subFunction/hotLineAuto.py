import os
import pandas as pd
import time
import pyautogui

#구동 명령 및 핫라인 대기열 호출
mailTriggerPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","4-1mailStart.json")
hotLinePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","4-4hotLine.json")

#Global 대기시간 설정
pyautogui.PAUSE = 0.5

#핫라인 전파
def hotLine(pressKey=int) -> None:
    time.sleep(0.5)
    pyautogui.click(x=20,y=20,clicks=1,button="left")
    pyautogui.click(x=400,y=215,clicks=1,button="left")
    pyautogui.press("down",presses=pressKey)
    pyautogui.press("enter")
    pyautogui.hotkey('ctrl','v')
    pyautogui.press("enter")
    pyautogui.press("esc")
    time.sleep(0.5)

if __name__ == "__main__":
    while True:
        time.sleep(0.2)
        startPoint = pd.read_json(mailTriggerPath,orient='records')
        if startPoint['hotline'].tolist()[0] == 'start':
            pressDown = pd.read_json(hotLinePath)[0].values.tolist()
            for i in pressDown:
                hotLine(i)
            pd.DataFrame({"coochip":"end","enMail":"end","hotline":"end"},index=[0]).to_json(mailTriggerPath,orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        else:
            pass