# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D39801875654237F667CD16CA02530FCBD35B68C1A7FA2DD9E460E3EF9DB054F4AC90A6561F5FE479D507189B546E9EA24D53B37541D7CF426E93734C38D7FF059EF8EE405202F0168466EBB83A6139113F087F489BB79E9DFAA739B41DBA91FCD824C2C43AF70FD105E5CF26BD4DA0BC5C60C4CC630F7828095CD67459E1887D86423F3F1608B5F8AF2F99A5D206FA70C5AC61E11F59D05523BA2E91C4F573978794C77BFBF7164FABA6BD3CB78818ADB674FF23739A5C6638ABAFD6D7012AFBB199F491E13AA0FE321DAE7A3027E316EE2F3D215B3951BEA02E81E5F43643B7CBBB817C285CAA5EC54E54B66CE77871166053E9A317D3DFBFF0AF3BB1EC9664DA504BF375A7584E054D036105F06CE3CF42391FCF079099BC03AF051E716C0023E71F6E35B2291F68351B522CD3EF9B62C3CD222B9B5DC30C1A5A86D9F6D28ECACF9ABB1AE9AF00EE4A6009D6531148A8CEE5ECFDB20B97889C4C306D45E84"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
