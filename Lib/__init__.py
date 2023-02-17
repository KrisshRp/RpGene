from .SeleniumDriver import Driver
from .NCBIscraper import NCBIscraper
from .module import *
from .chromeAutoDriverDownloader import ChromeDriverAutoDownloader
import os

def loadenv():
    for file in os.listdir("./Bin/env"):
        if ".env" in file:
            try:
                lines = open(f"./Bin/env/{file}").read().splitlines()
                for line in lines:
                    print(line)
                    if line !="" and "#" not in line:os.environ.update({line.split(" = ")[0]:line.split(" = ")[1]})
            except:pass
