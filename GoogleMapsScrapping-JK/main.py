from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import time
import pandas as pd

filename = "data.csv"

link = "https://www.google.com/maps/search/apparel/@-5.4009694,105.0857855,12z?entry=ttu"

browser = webdriver.Chrome()    
record = []
e = []
le = 0

def Selenium_extractor():
    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "TFQHme")

    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "TFQHme")

        if len(a) == var:
            le += 1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})
            name = Name_Html[0].text.strip()

            if name not in e:
                e.append(name)
                divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
                phone = next((div.text.strip() for div in divs if div.text.strip().startswith("+")), None)
                address = divs[0].text.strip()

                website = next((div.text.strip() for div in divs if div.text.strip().endswith(".com") or div.text.strip().endswith(".net")), "Not available")

                print([name, phone, address, website])
                record.append((name, phone, address, website))
        except Exception as e:
            print("error:", e)
            continue

    # Menyimpan DataFrame ke file CSV dalam mode append di luar loop for
    df = pd.DataFrame(record, columns=['Name', 'Phone number', 'Address', 'Website'])
    df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8')

try:
    browser.get(str(link))
    time.sleep(10)
    Selenium_extractor()
except Exception as e:
    print("error:", e)
finally:
    # Menutup browser
    browser.quit()