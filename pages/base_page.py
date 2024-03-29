from datetime import datetime

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    @allure.step('open page')
    def open(self):
        self.driver.get(self.url)
        # self.driver.maximize_window()
        self.driver.set_window_size(1920, 1080)

    def element_is_visible(self, locator, timeout=5):
        self.go_to_element(self.element_is_present(locator))
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator),
                                                         message=f"Can't see element by locator {locator}")

    def element_is_not_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator),
                                                         message=f"Can see element by locator {locator}")

    def elements_are_visible(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator),
                                                         message=f"Can't see element by locator {locator}")

    def element_is_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator),
                                                         message=f"Element not present by locator {locator}")

    def elements_are_present(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator),
                                                         message=f"Elements not present by locator {locator}")

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator),
                                                         message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator),
                                                         message=f"Can't find elements by locator {locator}")

    def element_is_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator),
                                                         message=f"Can't click element by locator {locator}")

    def go_to_element(self, element):
        self.driver.execute_script(
            "return arguments[0].scrollIntoView(true);", element)

    # browser.execute_script("return arguments[0].scrollIntoView(true);", button)
    @allure.step('alert_is_present')
    def alert_is_present(self, timeout=5):
        wait = WebDriverWait(self.driver, timeout)
        alert = wait.until(EC.alert_is_present(), message=f"Can't find alert")
        return alert

    @allure.step('action_double_click')
    def action_double_click(self, element):
        action = ActionChains(self.driver)
        action.double_click(element)
        action.perform()

    @allure.step('action_right_click')
    def action_right_click(self, element):
        action = ActionChains(self.driver)
        action.context_click(element)
        action.perform()


    @allure.step('action_drag_and_drop_offset')
    def action_drag_and_drop_offset(self, element, x_coord, y_coord):
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coord, y_coord)
        action.perform()

    @allure.step('action_drag_and_drop_to_element')
    def action_drag_and_drop_to_element(self, source, target):
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target)
        action.perform()

    @allure.step('action_move_to_element')
    def action_move_to_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    # remove banners
    @allure.step('remove_footer_and_banners')
    def remove_footer_and_banners(self):
        tab_name = self.driver.window_handles[0]
        try:
            self.driver.execute_script("document.getElementsByTagName('footer')[0].remove();")
            self.driver.execute_script("document.getElementById('close-fixedban').remove();")
            self.driver.execute_script("document.getElementById('adplus-anchor').remove();")
            self.driver.execute_script("document.getElementById('RightSide_Advertisement').remove();")
            self.driver.switch_to.frame(0)
            self.driver.execute_script("document.getElementById('google_image_div').remove();")
            self.driver.switch_to.window(tab_name)
        except:
            self.driver.switch_to.window(tab_name)
        # self.driver.execute_script("document.body.style.zoom = '0.75'")

    @allure.step('refresh_window')
    def refresh_window(self):
        self.driver.refresh()

    @allure.step('text_of_elements_list')
    def text_of_elements_list(self, elements_list):
        return [element.text for element in elements_list]

    @allure.step('get_background_color_element_hex')
    def get_background_color_element_hex(self, element):
        rgba = element.value_of_css_property('background-color')
        rgba_match = re.match(r'rgba\((\d+), (\d+), (\d+), (\d+)\)', rgba)
        if rgba_match:
            r, g, b, a = map(int, rgba_match.groups())
            return '#{r:02x}{g:02x}{b:02x}'.format(r=r, g=g, b=b)

    @allure.step('get_position_of_element')
    def get_position_of_element(self, element):
        left = float(element.value_of_css_property('left')[:-2])
        top = float(element.value_of_css_property('top')[:-2])
        return [left, top]

    @allure.step('get_size_of_element')
    def get_size_of_element(self, element):
        width = float(element.value_of_css_property('width')[:-2])
        height = float(element.value_of_css_property('height')[:-2])
        return [width, height]

    def allure_screenshot(self):
        attach = self.driver.get_screenshot_as_png()
        allure.attach(attach, name=f"Screenshot_{datetime.today()}", attachment_type=allure.attachment_type.PNG)

