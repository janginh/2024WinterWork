#1개는 읽는다
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Options 클래스 import
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_url_with_selenium(url):
    options = Options()  # Options 클래스 사용

    options.add_argument("--headless")  # 최소 옵션으로 시작

    # ChromeDriver 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        # 페이지 로딩 대기 시간 늘리기
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_source = driver.page_source.lower()  # 페이지 소스 가져오기

        if "교회" in page_source:
            return "교회 단어 발견"
        else:
            return "교회 단어 미발견"
    except Exception as e:
        return f"오류 발생: {str(e)}"
    finally:
        driver.quit()

# URL 테스트
url = "http://glorychurch.or.kr"
print(check_url_with_selenium(url))
