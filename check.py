# import libraries
import urllib2
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# specify the url
path_to_chromedriver = "/home/aadarsh/apple-iphonex/chromedriver/chromedriver"
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
browser.implicitly_wait(10) # seconds
url = "https://www.apple.com/shop/buy-iphone/iphone-x/5.8-inch-display-64gb-silver-t-mobile#00,12,30"
browser.get(url)
store_availability_button_xpath = ".//*[@id='main']/store-provider/step1-modular/materializer[2]/div[2]/div/summary-builder/div/div[2]/div[3]/div/div/div/div/div/button";
button = browser.find_element_by_xpath(store_availability_button_xpath)
print button.text