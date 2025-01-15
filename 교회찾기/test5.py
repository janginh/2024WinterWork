from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_url_with_selenium(url):
    # URL 형식 보정
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url.strip()
    
    options = Options()
    # Headless 모드를 제거해 실제 브라우저에서 확인
    # options.add_argument("--headless")  # 필요시 주석 처리
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"Trying to open URL: {url}")
        driver.get(url)

        # 페이지 로딩 대기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 페이지 소스에서 "교회"라는 단어 찾기
        page_source = driver.page_source.lower()
        if "교회" in page_source:
            return "교회 단어 발견"
        else:
            return "교회 단어 미발견"
    except Exception as e:
        return f"오류 발생: {str(e)}"
    finally:
        driver.quit()

# 테스트 URL
test_url = "http://gloryhrd.or.kr"
result = check_url_with_selenium(test_url)
print(result)
