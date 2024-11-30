import pyautogui
import time
import pandas as pd
def hotLine(Y=int) -> None:
    pyautogui.doubleClick(x=950,y=Y,interval=0.2)
    time.sleep(0.2)
    pyautogui.click(x=42,y=622,interval=0.2)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press("enter")
    pyautogui.press("esc")
    time.sleep(0.2)
if __name__ == "__main__":
    while True:
        time.sleep(0.2)
        startPoint = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json",orient='records')
        if startPoint['hotline'].tolist()[0] == 'start':
            Ypoint = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\4-4hotLine.json")[0].values.tolist()
            for i in Ypoint:
                hotLine(i)
            pd.DataFrame({"coochip":"end","enMail":"end","hotline":"end"},index=[0]).to_json('C:\\Users\\USER\\ve_1\\DB\\4-1mailStart.json',orient='records',force_ascii=False,indent=4)
            time.sleep(1)
        else:pass