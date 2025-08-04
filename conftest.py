import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

APP_ID = "bs://664aa316b184a8060e44cfbfa1477881660cf7a7"

devices = [
    {
        "deviceName": "Samsung Galaxy S23",
        "platformVersion": "13.0",
    },
    {
        "deviceName": "Google Pixel 7",
        "platformVersion": "13.0",  # <- FIXED from 12.0 to 13.0
    }
]

def get_driver(device, test_name):
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", device["deviceName"])
    options.set_capability("platformVersion", device["platformVersion"])
    options.set_capability("app", APP_ID)
    options.set_capability("bstack:options", {
        "projectName": "bs-demo-cert",
        "buildName": "Automate Build #123",
        "sessionName": test_name,
        "userName": os.environ["BROWSERSTACK_USERNAME"],
        "accessKey": os.environ["BROWSERSTACK_ACCESS_KEY"]
    })

    return webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options
    )

@pytest.fixture(params=devices, scope="function")
def driver(request):
    device = request.param
    driver = get_driver(device, request.node.name)
    yield driver
    driver.quit()
