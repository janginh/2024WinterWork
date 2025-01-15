from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# WebDriver Manager를 사용하여 ChromeDriver 자동 설치 및 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("http://www.google.com")
    print("페이지 제목:", driver.title)
finally:
    driver.quit()
