import logging, os, time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as webdtiver_with_proxy
from selenium.webdriver.remote.remote_connection import LOGGER
from ..chromeAutoDriverDownloader import ChromeDriverAutoDownloader
LOGGER.setLevel(logging.WARNING)

class Driver:
    def __init__(self, proxy = None, log = True, headless = False, executiveFilePath = None, extentionpath = None, windowSize = [1400, 1080], downloadPath="\Temp\dump"):
        options = Options()
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        if headless:options.add_argument('--headless')
        options.add_argument(f"window-size={windowSize[0]},{windowSize[1]}")
        if not log:options.add_experimental_option("excludeSwitches", ["enable-logging"])
        try:
            if extentionpath is not None: options.add_extension(extentionpath)
            elif len(os.listdir("./Bin/ext")) > 0:
                for ext in os.listdir("./Bin/ext"): options.add_extension(f"./Bin/ext/{ext}")
        except:pass

        if executiveFilePath is None:
            if sys.platform == "linux":
                obj = ChromeDriverAutoDownloader("/Bin/driver")
            if sys.platform == "win32":
                obj = ChromeDriverAutoDownloader("./Bin/driver")
            executiveFilePath = obj.driverPath

        if proxy is not None:
            options_seleniumWire = {'proxy': {'http': f"http://{proxy}",'https': f"http://{proxy}"}}
            self.driver = webdtiver_with_proxy.Chrome(options = options, executable_path = executiveFilePath, seleniumwire_options = options_seleniumWire, service_args=[f"--log-path=./temp/log/{round(time.time())}.log"])
        else:
            self.driver = webdriver.Chrome(options = options, executable_path = executiveFilePath)
