import os, requests, wget, zipfile, sys

class ChromeDriverAutoDownloader:
    def getSystemVersion(self):
        if sys.platform == "linux":
            regReply = os.popen('/usr/bin/google-chrome --version').read().replace("Google Chrome ", "").replace("\n", "")
        if sys.platform == "win32":
            regReply = os.popen(r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read().split("version")[-1].split(" ")[-1].replace("\n", "")
        return(regReply)

    def getDriverVersion(self):
        url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{self.getSystemVersion().split(".")[0]}'
        response = requests.get(url)
        version_number = response.text
        return(version_number)

    def download(self):
        yield(f"Downloading Chrome Driver [{self.getSystemVersion()}]")
        latest_driver_zip = wget.download(self.downloadLink, out=f'{self.driverLocation}/chromedriver.zip')
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(path = f'{self.driverLocation}/')
        os.remove(latest_driver_zip)
        try:os.rename(self.driver_binaryname, self.driverPath)
        except:os.remove(f"{self.driverLocation}/chromedriver.exe")
        os.chmod(self.driverPath, 755)
        yield("\n")
    
    def __init__(self, driverLocation="/"):
        self.driverLocation = f'{os.getcwd()}{driverLocation}'
        if sys.platform == "win32":
            self.downloadLink = f"https://chromedriver.storage.googleapis.com/{self.getDriverVersion()}/chromedriver_win32.zip"
            self.driver_binaryname = f'{self.driverLocation}/chromedriver.exe'
            self.driverPath = f'{self.driverLocation}/chromedriver-win-{self.getDriverVersion()}.exe'
        if sys.platform == "linux":
            self.downloadLink = f"https://chromedriver.storage.googleapis.com/{self.getDriverVersion()}/chromedriver_linux64.zip"
            self.driver_binaryname = f'{self.driverLocation}/chromedriver'
            self.driverPath = f'{self.driverLocation}/chromedriver-linux-{self.getDriverVersion()}'
            # print(self.driverPath.split("/"), (driverLocation))
        if self.driverPath.split("/")[-1] in os.listdir(self.driverLocation):
            print("Chrome Driver is up-to-dated")
        else:
            for i in self.download():print(i)