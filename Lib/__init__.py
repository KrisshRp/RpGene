from .SeleniumDriver import Driver
from .NCBIscraper import NCBIscraper
from .module import *
from .chromeAutoDriverDownloader import ChromeDriverAutoDownloader

import os

for file in os.listdir("./Bin/env"):
    if ".env" in file:
        try:
            lines = open(file).read().splitlines()
            for line in lines:
                if line !="" and "#" not in line:os.environ.update({line.split(" = ")[0]:line.split(" = ")[1]})
        except:pass