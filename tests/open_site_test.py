import time

from pages.base_page import BasePage

base_url = 'http://192.168.1.149/opencart/'


def test_open_site(driver):
    base_page = BasePage(driver, base_url)
    base_page.open()
    time.sleep(5)
    assert driver.current_url == base_url, 'Site Opencart was not opened'
