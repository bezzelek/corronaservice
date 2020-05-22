from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def get_firefox_config(download_path):
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", str(download_path))
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    return firefox_profile


def wait_for(file_path, wait_period=0.1, max_wait=60 * 2):
    total_wait = 0

    while not file_path.exists():
        if total_wait >= max_wait:
            raise ValueError("We're waiting too much!")

        sleep(wait_period)
        total_wait += wait_period


def download_csv(filename):
    download_folder = Path(__file__).parent.parent
    download_file = download_folder / filename

    if download_file.exists():
        download_file.unlink()

    with webdriver.Firefox(firefox_profile=get_firefox_config(download_folder)) as driver:
        driver.get("https://who.sprinklr.com/")
        presence = presence_of_element_located([By.XPATH, "//div[@role='button']/button"])
        download_button = WebDriverWait(driver, 30).until(presence)

        download_button.click()
        wait_for(download_file)
    return download_file
