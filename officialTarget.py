from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import userInput
import os
from twilio.rest import Client

account_sid = os.environ['REPLACE WITH UR ACCT SID']
auth_token = os.environ['REPLACE WITH UR AUTH TOKEN']
client = Client(account_sid, auth_token)

class TargetBot:
    def __init__(self):
        option = webdriver.ChromeOptions()
        # option.add_experimental_option("excludeSwitches", ["enable-automation"])
        # option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("window-size=1280,800")
        # option.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome("C:/Users/Emmanuel/PycharmProjects/TARGETEST/chromedriver.exe", options=option)
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

    def checkStock(self,link):
        refresh = True
        while refresh:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-test='orderPickupButton']"))
                )
                if 'Pick' not in element.text:
                    print("Still sold out")
                    refresh = True
                else:
                    message = client.messages.create(
                        body=f'The item you have requested is now in stock. Here is the link {link} ',
                        from_='###REPLACE WITH YOUR TWILIO NUMBER ###',
                        to='### REPLACE WITH END-USER PHONE NUMBER ###'
                    )
                    print(message.sid)
                    refresh = False
                    print("In stock")
            except:
                print("Still sold out.")
                refresh = True
            if refresh:
                self.driver.refresh()
            else:
                pass
        self.addtoCart(element)

    def addtoCart(self, element):
        element.click()
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@data-test='espModalContent-declineCoverageButton']"))
            ).click()
            self.driver.get('https://www.target.com/co-review')

        except:
            print("Couldn't decline insurance.")
            self.driver.get('https://www.target.com/co-review')

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
        return

    def enterPin(self, pin):
        tryAgain = True
        while tryAgain:
            try:
                pinSection = self.driver.find_element_by_id('creditCardInput-cvv')
                pinSection.send_keys(pin)
                print("Pin successful")
                tryAgain = False
            except:
                pass

    def confirmPin(self):
        tryAgain = True
        while tryAgain:
            try:
                element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@data-test='confirm-button']"))
                ).click()
                print("Pin has been confirmed.")
                tryAgain = False
            except:
                tryAgain = True
        return

    def saveContinue(self):
        tryAgain = True
        while tryAgain:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@data-test='save-and-continue-button']"))
                ).click()
                print("Saved and continue")
                tryAgain = False
                self.placeOrder()
            except:
                tryAgain = True


if __name__ == '__main__':
    userLink,userPin = userInput.userSubmission()
    print(userLink)
    a = TargetBot()
    a.openPage('https://target.com/')
    a.linkPage(userLink)
    a.checkStock(userLink)
    a.placeOrder()
    a.enterPin(userPin)
    a.confirmPin()
    a.saveContinue()
    a.saveContinue()
