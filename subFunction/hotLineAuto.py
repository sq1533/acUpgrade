import os
import pandas as pd
import time
import pyautogui
mailTriggerPath = os.path.join(os.path.dirname(__file__),"DB","4-1mailStart.json")
hotLinePath = os.path.join(os.path.dirname(__file__),"DB","4-4hotLine.json")
def hotLine(Y=int) -> None:
    pyautogui.doubleClick(x=950,y=Y,interval=0.2)
    pyautogui.click(x=42,y=622,interval=0.2)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press("enter")
    pyautogui.press("esc")
    time.sleep(0.2)
if __name__ == "__main__":
    while True:
        time.sleep(0.2)
        startPoint = pd.read_json(mailTriggerPath,orient='records')
        if startPoint['hotline'].tolist()[0] == 'start':
            Ypoint = pd.read_json(hotLinePath)[0].values.tolist()
            for i in Ypoint:
                hotLine(i)
            pd.DataFrame({"coochip":"end","enMail":"end","hotline":"end"},index=[0]).to_json(mailTriggerPath,orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        else:pass