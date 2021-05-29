import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import threading

class TargetBot:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("window-size=1280,800")
        option.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome("C:/Users/Emmanuel/Documents/chromedriver.exe", options=option)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.action = webdriver.ActionChains(self.driver)

    def openPage(self, link):
        self.driver.get(link)
        with open('cookies.txt', 'rb') as cookiesfile:
            cookies = json.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def linkPage(self, url):
        self.driver.get(url)

    def checkStock(self):
        refresh = True
        while refresh:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-test='orderPickupButton']"))
                )
                if 'Pick' not in element.text:
                    print("Still sold out")
                else:
                    refresh = False
                    print("In stock")
            except:
                print("Still sold out.")
                refresh = True
        self.addtoCart(element)

    def addtoCart(self, element):
        element.click()
        try:
                            #DECLINES INSURANCE
            element = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@data-test='espModalContent-declineCoverageButton']"))
            ).click()
                            #VIEW CART & CHECKOUT
            element = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@data-test='addToCartModalViewCartCheckout']"))
            ).click()
                            #GO TO FINAL CHECKOUT
            element = WebDriverWait(self.driver, 9).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@data-test='checkout-button']"))
            ).click()
            print("Decline insurance.")
            print("Now viewing cart")
        except:
            print("Couldn't decline insurance.")
        return

    def enterPin(self):
        tryAgain = True
        while tryAgain:
            try:
                pinSection = self.driver.find_element_by_id('creditCardInput-cvv')
                pinSection.send_keys('3608')
                print("Pin successful")
                tryAgain = False
            except:
                print("Couldn't find it.")

    def placeOrder(self):
        tryAgain = True
        while tryAgain:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@data-test='placeOrderButton']"))
                ).click()
                print("Order has been placed.")
                tryAgain = False
            except:
                tryAgain = True


def startThread():
    a = TargetBot()
    a.openPage('https://target.com/')
    a.linkPage(
        'https://www.target.com/p/dualsense-wireless-controller-for-playstation-5/-/A-83377785?preselect=81114477#lnk=sametab')
    a.checkStock()
    a.enterPin()
    a.placeOrder()