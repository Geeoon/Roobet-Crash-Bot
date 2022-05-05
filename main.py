import credentials
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

MAX_TIMEOUT = 50
WINDOW_LOCATION = (0, 0)
ADD = 0
BET_AMNT = 1  # dollars
BET_WAIT = 1.25  # seconds
DEMO_MODE = False
if DEMO_MODE:
    BET_AMNT = 0
    ADD = 30
chop = webdriver.ChromeOptions()
chop.add_argument("--disable-extensions");
chop.add_argument("test-type");
chop.add_argument("window-size=595,850")
chop.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chop)
browser.set_window_position(WINDOW_LOCATION[0], WINDOW_LOCATION[1], windowHandle='current')

browser.get("https://roobet.com/?modal=auth&tab=login")

# log in
try:
    element = WebDriverWait(browser, MAX_TIMEOUT).until(ec.presence_of_element_located((By.ID, r'auth-dialog-username')))
finally:
    browser.find_element(by=By.ID, value=r'auth-dialog-username').send_keys(credentials.EMAIL)
    browser.find_element(by=By.ID, value=r'auth-dialog-current-password').send_keys(credentials.PASSWORD)
    browser.find_element(by=By.ID, value=r'auth-dialog-current-password').send_keys(Keys.ENTER)

time.sleep(10)  # wait in case of captcha
browser.get("https://roobet.com/crash")
time.sleep(5)
pyautogui.leftClick(x=300, y=700)
for i in range(5):
    pyautogui.press('backspace')

pyautogui.typewrite(str(BET_AMNT))
pyautogui.leftClick(x=300, y=750)
for i in range(5):
    pyautogui.press('backspace')

pyautogui.typewrite("9999")

while 1:
    start_time = 0
    while 1:
        if pyautogui.pixel(400, 800 + ADD) == (230, 190, 88):
            pyautogui.leftClick(x=400, y=800 + ADD)
            pyautogui.moveTo(300, 700)
            start_time = 0
            break
        elif pyautogui.pixel(400, 800 + ADD) == (97, 175, 96):
            if start_time == 0:
                start_time = time.time()
            if time.time() - start_time >= BET_WAIT:
                pyautogui.leftClick(x=400, y=800 + ADD)
                pyautogui.moveTo(300, 700)
                break
# yellow: (230, 190, 88)
# red: (243, 69, 60)
# green: (97, 175, 96)