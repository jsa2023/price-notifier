from selenium import webdriver
import os
from datetime import datetime as dt
import smtplib
from email.mime.text import MIMEText

def get_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://www.amazon.com/PF-WaterWorks-PF0989-Disposal-Installation/dp/B078H38Q1M/")
  return driver

def get_price(driver):
  element = driver.find_element(by="id",value="corePrice_desktop")
  text = element.text
  price = text.replace("Price:\n","").replace("$","")
  #print(price)
  return float(price)

def get_previous_price(price):
  date = dt.now().strftime('%m/%d/%Y')
  if (os.path.exists('price.txt')):
    with open('price.txt', 'r') as f:
      previous_price = float(f.read().split(': ')[1].replace("$",""))
  else:
    with open('price.txt', 'w') as f:
      sentence = f"price as of {date}: $" + str(price)
      f.write(sentence)
      previous_price = price
  return previous_price

def send_email(receiver, price):
  sender = os.getenv('email_addr')
  password = os.getenv('PASSWORD')
  message = """
      This is to inform you that the price of the product 
      PF WaterWorks PF0989 Garbage Disposal Installation Kit, White is now ${}
      """.format(price)
  message = MIMEText(message)
  message['From'] = sender
  message['To'] = receiver
  message['Subject'] = 'Change notification'

  server = smtplib.SMTP('smtp.office365.com', 587)
  server.starttls()
  server.login(sender, password)
  server.sendmail(sender, receiver, message.as_string())
  server.quit()

def add_new_price(price):
  date = dt.now().strftime('%m/%d/%Y')
  with open('price.txt', 'w') as f:
    sentence = f"price as of {date}: $" + str(price)
    f.write(sentence)

def main():
  driver = get_driver()
  price = get_price(driver)
  previous_price = get_previous_price(price)
  if (price != previous_price):
    send_email('xbxhakbxbxceodijbj@nvhrw.com',price)
    add_new_price(price)

print(main())