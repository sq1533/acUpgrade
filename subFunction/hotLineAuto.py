import pyautogui
import time
import pandas as pd
#print(pyautogui.position())
#핫라인 메세지 보내기
def hotLine(X=int):
    pyautogui.doubleClick(x=X,y=300,interval=0.2)
    pyautogui.click(x=20,y=950,interval=0.2)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press("enter")
    pyautogui.press("esc")
    time.sleep(0.2)

if __name__ == "__main__":
    while True:
        startPoint = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json",orient='records')
        if startPoint['hotline'].tolist()[0] == 'start':
            Xpoint = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-4hotLine.json")[0].values.tolist()
            for i in Xpoint:hotLine(i)
            pd.DataFrame({"coochip":"end","enMail":"end","hotline":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        else:
            pyautogui.moveTo(400,600)
            time.sleep(0.5)
            pyautogui.moveTo(600,400)
            time.sleep(0.5)
            pass