from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

kb_list = [
    "KB82139", "KB772759", "KB790991", "KB126082", "KB164685", "KB124778", "KB706280", "KB151428",
    "KB135426", "KB114508", "KB466867", "KB146995", "KB64649", "KB86521", "KB829402", "KB151276",
    "KB140138", "KB743048", "KB112130", "KB709491", "KB130871", "KB829512", "KB138896", "KB186360",
    "KB470658", "KB863647", "KB135682", "KB186752", "KB236559", "KB186639", "KB186596", "KB187128",
    "KB109815", "KB627589", "KB144853", "KB135161", "KB168175", "KB186553", "KB152035", "KB187091",
    "KB67612", "KB135063", "KB516950", "KB859947", "KB118933", "KB186275", "KB278867", "KB147381",
    "KB816548", "KB779304", "KB186428", "KB837912"
]

output_folder = "oracle_kbs"
os.makedirs(output_folder, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("Open any Oracle Support page and log in manually if needed.")
driver.get("https://support.oracle.com/")
input("After logging in, press Enter...")

for kb_id in kb_list:
    kb_url = f"https://support.oracle.com/ic/builder/rt/customer_portal/live/webApps/customer-portal/?kmExternalId={kb_id}"
    print(f"Checking {kb_url}")
    driver.get(kb_url)
    time.sleep(10)
    html = driver.page_source
    if "Article not found" not in html and "does not exist" not in html:
        file_path = os.path.join(output_folder, f"{kb_id}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved: {file_path}")
    else:
        print(f"{kb_id} not found or not accessible.")

driver.quit()