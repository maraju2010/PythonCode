from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.ie.options import Options
import time
import sys
import logging
import base64
import configparser
from selenium.webdriver.common.keys import Keys


logging.getLogger(__name__)

class Browser(object):
    global logger
    def __init__(self):
        #self.browser = webdriver.Chrome()
        try:
            if self._OS_read_config()=="64":
                EXE_PATH = r'IE64\IEDriverServer.exe'
                #self.browser = webdriver.Ie(executable_path=EXE_PATH,capabilities={'ignoreZoomSetting':True,'ignoreProtectedModeSettings':True})
                ie_options = Options()
                ie_options.ignore_protected_mode_settings = True
                ie_options.ignore_zoom_level = True
                self.browser = webdriver.Ie(executable_path=EXE_PATH,options=ie_options)
                logging.info("Succesfully loaded 64 bit IE driver")
            else:
                EXE_PATH = r'IE32\IEDriverServer.exe'
                ie_options = Options()
                ie_options.ignore_protected_mode_settings = True
                ie_options.ignore_zoom_level = True
                self.browser = webdriver.Ie(executable_path=EXE_PATH,options=ie_options)
                logging.info("Succesfully loaded 32 bit IE driver")
        except Exception as e:
            logging.debug("failed initializing webdriver %s" %e)

    def run(self,finesseurl):
        try:
            self.browser.get(finesseurl)
        except Exception as e:
            logging.debug("failed to get browser url %s" %e)

    def login(self,username,password,extension):
        try:
            uname_handle = self.browser.find_element_by_id('username')
            pwd_handle = self.browser.find_element_by_id('password')
            ext_handle = self.browser.find_element_by_id('extension')
            #loginbutton_handle = self.browser.find_element_by_id('signin-button')
            loginbutton_handle = self.browser.find_element_by_id('signin-button')
            uname_handle.clear()
            uname_handle.send_keys(username)
            pwd_handle.clear()
            pwd_handle.send_keys(password)
            ext_handle.send_keys(extension)
            #loginbutton_handle.click()
            #loginbutton.send_keys("\n")
            self.browser.execute_script("arguments[0].click()", loginbutton_handle)

        except TimeoutException:
            logging.debug("timed out waiting for alert %s" %e)

        except Exception as e:
            logging.debug("failed with error while logging %s" %e)

    def checkelement(self):
        try:
            html = self.browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            return html
        except NoSuchWindowException as i:
            logging.debug("failed with error %s" % i)
            return "NoSuchWindowException"
        except Exception as e:
            logging.debug("failed check element %s" %e)

    def get_credentials(self):
        try:
            return self.browser.find_element_by_id('user-info-text').text
        except Exception as e:
            logging.debug("failed get credentials %s" %e)

    def recheck_credentials(self):
        try:
            gadget = self.browser.find_element_by_id('finesse_gadget_1').text
            gadgetlist = gadget.split(";")
            username,password,extension=self.get_gadget(gadgetlist)
            return username,password,extension
        except Exception as e:
            logging.debug("failed recheck credentials %s" %e)

    def _close(self):
        try:
            self.browser.quit()
            logging.info("closing browser...%s" % self.browser)
        except Exception as e:
            logging.debug("caught exception while closing %s" %e)

    def get_gadget(self,templist):
        try:
            userid=""
            pwd=""
            ext=""
            for i in templist:
                if "up_id" in i:
                    ignore,userid = i.split("=")
                    if userid:
                        pwd=userid
                if  "up_extension" in i:
                    ignore1,extension = i.split("=")
            return userid,pwd,extension
        except Exception as e:
            logging.debug("caught exception while closing %s" %e)

    def hack_password(self):
        try:
            sessionstorage = self.browser.execute_script("return sessionStorage.getItem('userFinesseAuth');");
            #sessionstorage = self.browser.execute_script("return Object.keys(sessionStorage);");
            user,pwd = self._parse_credentials(sessionstorage)
            return user,pwd
        except Exception as e:
            logging.debug("caught exception while closing %s" %e)

    def _parse_credentials(self,sessionstorage):
        decoded_data = base64.b64decode(sessionstorage)
        username,password = decoded_data.decode("utf-8").split(":")
        return username,password

    def _OS_read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read("ConfigProperty.ini")
            Platform = dict(config.items('Platform'))
            #print(Platform)
            OSBIT = Platform.get('windowsbit')
            return OSBIT
        except Exception as e:
            logging.debug("caught exception while closing %s" %e)

    def reattempt(self):
        try:
            ok_handle = self.browser.find_element_by_class_name("ui-button-text")
            self.browser.execute_script("arguments[0].click()", ok_handle)
        except Exception as e:
            logging.debug("caught exception while closing %s" %e)
