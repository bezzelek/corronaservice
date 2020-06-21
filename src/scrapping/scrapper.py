""" Module to scrap data for the project. """

from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def get_config(download_path: Path) -> Options:
    """ Function with parameters of web-driver which is needed to download data.

    :param download_path: Path to the directory to download file.
    :return: Preferences of firefox_profile which is needed to download data.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": str(download_path),
        "download.prompt_for_download": False,
    })
    return chrome_options

def wait_for(file_path: Path, wait_period: float = 0.1, max_wait: int = 60 * 2) -> None:
    """ Function that waits for downloading file.

    :param file_path: path to downloaded file
    :param wait_period: timeouts between retries
    :param max_wait: maximum time of waiting for downloading
    """
    total_wait = 0.0

    while not file_path.exists():
        if total_wait >= max_wait:
            raise ValueError("We're waiting too much!")

        sleep(wait_period)
        total_wait += wait_period


def download_csv(filename: str) -> Path:
    """ Function that downloads file with data.

    :param filename: Name of the downloading file.
    :return: Path to downloaded file.
    """
    download_folder = Path(__file__).parent.parent
    download_file = download_folder / filename

    if download_file.exists():
        download_file.unlink()

    with webdriver.Chrome(options=get_config(download_folder)) as driver:
        driver.get("https://who.sprinklr.com/")
        presence = presence_of_element_located([By.XPATH, "//div[@role='button']"])
        download_button = WebDriverWait(driver, 30).until(presence)

        download_button.click()
        wait_for(download_file)
    return download_file
