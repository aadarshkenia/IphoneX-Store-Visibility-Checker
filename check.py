# import libraries
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, time
import time as Time
import logging
import requests


def send_sms(from_, to, message, api_key, api_secret):
	print "Sending message."
	base_url="https://rest.nexmo.com/sms/json"
	payload = {"from": from_, "text": message, "to": to, "api_key": api_key, "api_secret": api_secret}
	logger.info("Request payload: %s", payload)
	response = requests.post(base_url, data=payload)
	logger.info("Send message response: %s", response)

def read_up_config(file):
	separator = "="
	dict = {}
	with open(file) as f:
		for line in f:
			if separator in line:
				name, value = line.split(separator, 1)
				dict[name.strip()] = value.strip()
		f.close()
		return dict;

def is_time_in_interval(start, end):
	time_now = datetime.now().time()
	logger.info("current time: %s", time_now)
	logger.info("start time: %s", start)
	logger.info("end time: %s", end)
	if time_now >= start and time_now <= end:
		return True
	return False

#setup logging config
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='./logs/myapp.log',
                    filemode='a')
logger = logging.getLogger(__name__)

now = datetime.now()
now_time = now.time()
if now_time >= time(10,30) and now_time <= time(16,30):
    print "yes, within the interval"


#Initialize config.
config = read_up_config("appConfig.properties")
logger.info("Configuration file read as: %s", config)

start = time(6,0)
end = time(7,30)

maxCounter = 15
counter = 0

time_between_checks=1800 #seconds
total_messages_sent = 0
while counter < maxCounter:
	logger.info("Checking for counter=%d", counter)
	try:
		# specify the url
		counter += 1
		product_url = "https://www.apple.com/shop/buy-iphone/iphone-x/5.8-inch-display-64gb-silver-t-mobile#00,12,30"
		path_to_chromedriver = "/home/aadarsh/apple-iphonex/chromedriver/chromedriver"
		browser = webdriver.Chrome(executable_path = path_to_chromedriver)
		browser.get(product_url)

		#get button to check store availability
		store_availability_button_xpath = ".//*[@id='main']/store-provider/step1-modular/materializer[2]/div[2]/div/summary-builder/div/div[2]/div[3]/div/div/div/div/div/button";
		wait = WebDriverWait(browser, 10)
		store_availability_button = wait.until(EC.element_to_be_clickable((By.XPATH, store_availability_button_xpath)))
		logger.info("Store availability check element found with text: " + store_availability_button.text)

		#perform button click.
		webdriver.ActionChains(browser).move_to_element(store_availability_button).click().perform()
		logger.info("Button click performed!")

		Time.sleep(5)

		availability_list_xpath = "/html/body/overlay[8]/materializer/div/div/product-locator/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/button/span[1]"
		availability_list_span = wait.until(EC.presence_of_element_located((By.XPATH, availability_list_xpath)))
		availability_text = availability_list_span.text
		logger.info("Availability check: " + availability_text)

		if is_time_in_interval(start, end) and total_messages_sent <= 2:
			message_text = ""
			if availability_text.startswith("Not available"):
				message_text = "NO Iphone X availability found."
			else:
				message_text = "Iphone X looks to be available. Check online immediately."
			send_sms(config["nexmo_sender_unique_id"], "13475533244", message_text, config["nexmo_api_key"], config["nexmo_api_secret"])
			total_messages_sent += 1
		else:
			logger.info("Time is not in interval, skipping sending of text message")

	except TimeoutException as ex:
		print("Exception has been thrown. " + str(ex))
	finally:
		browser.close()
		Time.sleep(time_between_checks)