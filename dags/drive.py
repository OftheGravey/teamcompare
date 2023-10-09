from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def drive():
    browser = webdriver.Remote(command_executor='http://192.168.1.152:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    print("T")
    return browser.get('http://www.google.com') 

drive()