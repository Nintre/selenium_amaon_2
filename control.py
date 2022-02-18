import os
import sys
import time

from selenium import webdriver
import setting

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_driver():
    try:
        chrome_options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)

        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("disable-web-security")
        chrome_options.add_argument('disable-infobars')

        chrome_options.headless = setting.HEADLESS

        chrome_options.add_argument(
            'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"')
        chrome_options.add_argument('Accept-Language="en"')
        chrome_options.add_argument('Connection="keep-alive"')

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(setting.CHROME_WEBDRIVER_PATH, options=chrome_options)

        return driver
    except Exception as e:
        print("get_driver:", e)


def change_address(driver, postal):
    while True:
        try:
            driver.find_element_by_id('glow-ingress-line1').click()
            time.sleep(1)
        except Exception as e:
            print("click配送至出错! or验证码界面!")
            driver.refresh()
            continue
        try:
            driver.find_element_by_id("GLUXChangePostalCodeLink").click()
            time.sleep(2)
        except:
            pass
        try:
            driver.find_element_by_id('GLUXZipUpdateInput').send_keys(postal)
            break
        except Exception as NoSuchElementException:
            try:
                driver.find_element_by_id('GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                driver.find_element_by_id('GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                print('NoSuchElementException err:', NoSuchElementException)
                driver.refresh()
                time.sleep(1)
                continue
    driver.find_element_by_id('GLUXZipUpdate').click()
    time.sleep(1)
    driver.refresh()


def search_keywords(driver, keywords):
    while True:
        try:
            driver.find_element_by_id('twotabsearchtextbox').clear()
            driver.find_element_by_id('twotabsearchtextbox').send_keys(keywords)
            driver.find_element_by_id('nav-search-submit-button').click()
            break
        except Exception as e:
            print("search_keywords:", e)
            driver.refresh()
            continue
    return driver
