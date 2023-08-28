import pytest
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from selenium.webdriver.edge.options import Options as OptionsEdge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: '--browser_name=chrome' or '--browser_name=firefox'")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language: '--language=en' or '--language=ru'")

    parser.addoption('--headless', action='store_true',
                     help="Headless mod: '--headless'")


# это добавит возможность писать параметры в коммандной строке:
# pytest -s -v --browser_name=firefox --language=ru


# добавляем параметр запуска тестов в командной строке(чем запускать, хромом или фаерфоксом) По умолчанию хром
# parser.addoption('--browser_name', action='store', default=None, help="Choose browser: chrome or firefox")
# Можно задать значение параметра по умолчанию,
# чтобы в командной строке не обязательно было указывать параметр --browser_name, например, так:

# Запуск браузера(для каждой функции)
@pytest.fixture(scope="function")  # по умолчанию запускается для каждой функции
def driver(request):
    browser_name = request.config.getoption(
        "browser_name")  # получаем параметр командной строки browser_name
    user_language = request.config.getoption("language")
    headless = request.config.getoption("--headless")
    # headless = True  # режим браузера без отображения (безголовый)
    # headless = False  # режим с отображением браузера

    if browser_name == "chrome":
        chrome_options = OptionsChrome()
        if headless:
            chrome_options.add_argument('--headless')  # Включение режима headless
        chrome_options.add_experimental_option(
            'prefs', {'intl.accept_languages': user_language})
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    elif browser_name == "firefox":
        options_firefox = OptionsFirefox()
        options_firefox.page_load_strategy = "eager"  # 'normal'
        options_firefox.add_argument('--language')
        # !!!
        # безголовый режим браузера задается переменной headless
        if headless:
            options_firefox.add_argument("--headless")  # ?похоже, не работает на MacOS
        driver = webdriver.Firefox(
            service=webdriver.firefox.service.Service(
                executable_path=GeckoDriverManager().install(),
                log_output="geckodriver.log"  # Specify the desired log output file
            ),
            options=options_firefox
        )

    elif browser_name == "edge":
        options_edge = OptionsEdge()
        options_edge.page_load_strategy = "eager"  # 'normal'
        options_edge.add_argument('--language')
        if headless:
            options_edge.add_argument('--headless')  # Включение режима headless
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options_edge)

    else:
        raise pytest.UsageError("--browser_name should be chrome, firefox or edge")
    yield driver
    driver.quit()
