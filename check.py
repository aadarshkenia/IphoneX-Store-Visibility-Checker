# import libraries
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logging


#setup logging config
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='./logs/myapp.log',
                    filemode='a')
logger = logging.getLogger(__name__)

# specify the url
product_url = "https://www.apple.com/shop/buy-iphone/iphone-x/5.8-inch-display-64gb-silver-t-mobile#00,12,30"
path_to_chromedriver = "/home/aadarsh/apple-iphonex/chromedriver/chromedriver"
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
browser.get(product_url)

#get button to check store availability
store_availability_button_xpath = ".//*[@id='main']/store-provider/step1-modular/materializer[2]/div[2]/div/summary-builder/div/div[2]/div[3]/div/div/div/div/div/button";
wait = WebDriverWait(browser, 10)
store_availability_button = wait.until(EC.presence_of_element_located((By.XPATH, store_availability_button_xpath)))
logger.debug("Store availability check element found with text: " + store_availability_button.text)

#quit gracefully
logger.debug("Closing browser !!")
browser.close()