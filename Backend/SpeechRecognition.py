from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options  import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By

Link = r'C:\Users\bhatt\OneDrive\Desktop\Jarvis\Backend\Voice.html'
chrome_options =  webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--use-fake-ui-for-media-stream") # To enable the microphone in head
chrome_options.add_argument("--use-fake-device-for-media-stream") # For camera

service = Service(ChromeDriverManager().install())
driver =  webdriver.Chrome(service=service, options=chrome_options)
driver.get(Link)
sleep(2)

def SpeechRecognition():
    driver.find_element(by=By.ID,value="start").click()
    print("Listening...")

    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text
            if Text:
                driver.find_element(by=By.ID, value= "end").click()
                return Text
            else:
                sleep(0.222)
        except Exception as e:
            print(e)


