import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class GlobalState:
    is_logged_in = False

chrome_options = Options()

# ------------------------------------------------------------
# UNIVERSAL flags (safe on Windows, Linux, macOS)
# ------------------------------------------------------------
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-allow-origins=*")

# Chrome 115+ strict profile system — required on Linux, harmless on Windows
chrome_options.add_argument("--disable-features=UserDataDirPreferences,UserDataDirEnhanced")

# ------------------------------------------------------------
# CROSS-PLATFORM SAFE TMP PROFILE (THIS FIXES THE ERROR)
# ------------------------------------------------------------
profile_root = tempfile.mkdtemp()
default_dir = os.path.join(profile_root, "Default")
os.makedirs(default_dir, exist_ok=True)

chrome_options.add_argument(f"--user-data-dir={profile_root}")

# ------------------------------------------------------------
# Downloads folder (cross-platform safe)
# ------------------------------------------------------------
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# ------------------------------------------------------------
# Create driver
# ------------------------------------------------------------
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

long_waits = WebDriverWait(driver, 60, poll_frequency=2)
short_waits = WebDriverWait(driver, 15, poll_frequency=1)
