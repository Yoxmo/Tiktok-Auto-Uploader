import time
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import shutil 
import pickle
from os.path import exists
import os, shutil
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common
import undetected_chromedriver.v2 as uc
from fake_useragent import UserAgent, FakeUserAgentError


class Cookies:
    def __init__(self, bot):
        self.bot = bot
        self.cookies_dir = os.path.join(os.getcwd(), "modules")
        if not exists(self.cookies_dir):
            os.mkdir(self.cookies_dir)
        self.selectCookie()


    def selectCookie(self):
        if len(os.listdir(self.cookies_dir)) > 0:
            cookies_dict = dict(enumerate(os.listdir(self.cookies_dir)))
            selected_cookie = cookies_dict[0]
            self.loadCookies(selected_cookie)
        else:
            print("No cookies stored on save directory!")
            self.createCookie()


    def loadCookies(self, selected_cookie):
        # Using chrome, sameSite cookie must not be set to None due to Google's policy.
        cookie_path = os.path.join(self.cookies_dir, selected_cookie)
        cookie_data = pickle.load(open(cookie_path, "rb"))
        for cookie in cookie_data:
            if 'sameSite' in cookie:
                if cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
            self.bot.add_cookie(cookie)

    def createCookie(self):
        print("Your browser currently shows the tiktok login page, please login in.")
        input("After you have logged in fully, please press any button to continue...")
        print("#####")
        filename = input("Please enter a name for the cookie to be stored as::: ")
        cookie_path = os.path.join(self.cookies_dir, filename+".cookie")
        pickle.dump(self.bot.get_cookies(), open(cookie_path, "wb+"))
        print("Cookie has been created successfully, resuming upload!")

class Browser:
    def __init__(self):
        try:
            ua = UserAgent()
            self.user_agent = ua.random
        except FakeUserAgentError:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = uc.ChromeOptions()
        # options.add_argument("--user-agent=" + self.user_agent)
        self.bot = uc.Chrome(options=options)
        self.bot.delete_all_cookies()

    def getBot(self):
        return self.bot

class Bot:
    """Bot used as high level interaction with web-browser via Javascript exec"""
    def __init__(self, bot):
        self.bot = bot

    def getBot(self):
        return self.bot

    def getVideoUploadInput(self):
        self.browser.WebDriverWait(self.browser, 10).until(self.browser.EC.presence_of_element_located((self.browser.By.TAG_NAME, "iframe")))
        self.browser.switch_to.frame(0)
        self.browser.implicitly_wait(1)
        file_input_element = self.browser.find_elements(self.browser.By.CLASS_NAME, "upload-btn-input")[0]
        return file_input_element

    def uploadButtonClick(self):
        try:
            """Newer layout."""
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "op-part-v2")))
            operation_elems = self.bot.find_elements(By.CLASS_NAME, "op-part-v2")[0]
            upload_elem = operation_elems.find_elements(By.XPATH, './*')[1]
            upload_elem.click()
        except Exception as e:
            try:
                upload_name = "Post"
                self.bot.find_element(By.XPATH, f'//button[text()="{upload_name}"]')
            except Exception as e:
                try:
                    """Older Layout"""
                    self.click_elem(
                        'document.getElementsByClassName("btn-post")[0].click()',
                        "Javascript had trouble finding the post button with given selector,"
                        " please submit yourself and edit submit button placement.!!")
                except Exception as e:
                    print("Could not upload, please upload manually.")


    def click_elem(self, javascript_script, error_msg):
        try:
            self.bot.execute_script(javascript_script)
        except selenium.common.exceptions.JavascriptException as je:
            print(error_msg)
            print(je)
        except Exception as e:
            print(f"Unhandled Error: {e}")
            exit()
        return

class Upload:
    def __init__(self, user):
        self.bot = None
        self.lang = "en"
        self.url = f"https://www.tiktok.com/upload?lang={self.lang}"
        self.cookies = None
        self.userRequest = {"dir": "", "cap": "", "vidTxt": ""}
        self.video = None
        self.videoFormats = ["mov", "flv", "avi"]
        self.userPreference = user

    def directUpload(self, filename):
        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)
        self.bot.get(self.url)
        time.sleep(5)
        self.cookies = Cookies(self.bot)
        self.bot.refresh()

        filenamex = r'C:\Users\ymamo\Documents\Temporary\dax\EXT\Tiktok\video-0.mp4'

        try:
            file_input_element = self.webbot.getVideoUploadInput()

            self.bot.implicitly_wait(5)

            file_input_element.send_keys(filenamex)

        except Exception as e:
            print(f"Error: {e}")
            print("Major error, Direct Upload Function.")

        time.sleep(5)
        time.sleep(5)
        time.sleep(5)
        time.sleep(5)

        self.webbot.uploadButtonClick()
            
        time.sleep(95)
        os.unlink('video.mp4')
        exit(0)

class User:
    def _checkFileDirExist(self, video_save_dir):
        os.makedirs(video_save_dir, exist_ok=True)

class TiktokBot:
    def __init__(self, video_save_dir=None):
        self.user = User() if not video_save_dir else User(video_save_dir)
        self.upload = Upload(self.user)
        self.dir = video_save_dir
        self.clearDir()

    def clearDir(self):
        if self.dir:
            shutil.rmtree(self.dir)
            os.makedirs(self.dir)

if __name__ == '__main__':
    tiktok_bot = TiktokBot() 
    tiktok_bot.upload.directUpload("video-0.mp4")