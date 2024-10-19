import random
from websockets.sync.client import connect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from websocket import WebSocketTimeoutException
import string
import time
import os

# Set up the Selenium WebDriver (make sure to have the correct WebDriver for your browser)


def get_driver():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    See https://nander.cc/using-selenium-within-a-docker-container
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-background-timer-throttling")
    # chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    # chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "/tmp",  # Change default download directory
            "download.prompt_for_download": False,  # Don't prompt for download
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,  # Enable safe browsing
        },
    )
    service = ChromeService(executable_path="/usr/bin/chromedriver")

    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return webdriver.Chrome(options=chrome_options, service=service)


driver = get_driver()
driver.implicitly_wait(2)

url = "http://irc.local:1337/"

class TestIrcFrontend:
    def test_ui_signup(self):
        driver.get(f"{url}/signup")
        time.sleep(0.5)  # Wait for the page to load

        # Fill in the signup form
        username = "".join(random.choices(string.ascii_letters, k=8))
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirmPassword").send_keys("password123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]").click()

        time.sleep(2)  # Wait for redirection or form submission

        # Check if redirected to the main page
        assert "Create Room" in driver.page_source

    def test_ui_create_room(self):
        # Assuming the user is logged in
        # Create a room
        room_name = "Test Room"
        driver.find_element(By.ID, "roomName").send_keys(
            room_name
        )  # Assuming there's an input for room name
        driver.find_element(
            By.XPATH, "//button[contains(text(), 'Create Room')]"
        ).click()  # Submit button for room creation
        time.sleep(0.5)
        driver.get(f"{url}/")
        time.sleep(0.5)  # Wait for room creation to process
        driver.find_element(
            By.XPATH, f"//span[contains(text(), '{room_name}')]"
        ).click()
        assert room_name in driver.page_source  # Check if room appears

    def test_ui_upload_file(self):
        with open("/tmp/test.txt", "wt") as f:
            f.write("""my cool file""")
        svg_file_path = os.path.abspath("/tmp/test.txt")
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
            svg_file_path
        )  # Assuming there's an input for file upload
        driver.find_element(
            By.XPATH, "//button[contains(text(), 'Send')]"
        ).click()  # Send button for file upload

        time.sleep(0.5)  # Wait for the file to be sent

        # Verify if the txt appears in the chat (you will need to implement a way to display uploaded files)
        assert (
            "test.txt" in driver.page_source
        )

        # Click on the txt link (you may need to adjust the selector)
        txt_link = driver.find_element(By.XPATH, "//a[contains(text(), 'test.txt')]")
        txt_link.click()

        time.sleep(0.5)  # Wait for the SVG content to load
        assert os.path.isfile("/tmp/test.txt")
