import time
from selenium import webdriver
import json
from time import sleep
from tqdm import tqdm


class TargetBot:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument("window-size=1280,800")
        self.driver = webdriver.Chrome("C:/Users/Emmanuel/Documents/chromedriver.exe", options=option)
        self.action = webdriver.ActionChains(self.driver)

    def openPage(self, link):
        self.driver.get(link)
        for i in tqdm(range(20)):
            sleep(1)
        with open('cookies.txt', 'w') as cookieFile:
            json.dump(self.driver.get_cookies(), cookieFile)
        return

    def linkPage(self, url):
        self.driver.get(url)


if __name__ == '__main__':
    a = TargetBot()
    a.openPage('https://target.com/')
    a.driver.close()
    quit()
