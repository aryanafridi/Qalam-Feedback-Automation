from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from seleniumbase import SB
from seleniumbase import BaseCase
import subprocess
import time
import os
import platform


TEMP_PROFILES = {
    "WINDOWS": os.path.expanduser("~/AppData/Local/Temp/ProfileTemp"), 
    "LINUX": "/tmp/ProfileTemp"
}


class BrowserHandler:
    def __init__(self, temp_profile: str = None) -> None:
        """Handling chrome browser startup and all options for browser handling."""

        self.platform = platform.system().upper()
        self.temp_profile = temp_profile if temp_profile is not None else TEMP_PROFILES[self.platform]
        self.sb_init: SB
        self.driver: Chrome
        self.wait: WebDriverWait
    
    def start_chrome(self, headless: bool = False) -> None:
        """Start Chrome Browser."""

        self.sb_init = SB(uc=True, headed = not headless, user_data_dir=self.temp_profile)
        sb: BaseCase = self.sb_init.__enter__()
        self.driver = sb.driver
        self.wait = WebDriverWait(self.driver, 40)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(300)
    
    def kill_browser(self, delete_profile: bool = True) -> None:
        """Kill browser and delete profile."""

        self.driver.quit()
        self.sb_init.__exit__(None, None, None)
        time.sleep(5)
        if not delete_profile:
            return
        if self.platform == "LINUX":
            subprocess.Popen(fr"rm -r {self.temp_profile}", shell=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL)
        elif self.platform == "WINDOWS":
            subprocess.Popen(fr'rmdir /S /Q {self.temp_profile}', shell=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                            stdin=subprocess.DEVNULL)
