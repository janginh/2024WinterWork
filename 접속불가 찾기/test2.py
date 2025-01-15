from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

def check_url_with_selenium(url):
    # Selenium Chrome 설정
    options = Options()
    options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # WebDriver Manager로 ChromeDriver 자동 설치
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        page_source = driver.page_source.lower()  # 페이지 소스 가져오기 (소문자로 변환)

        # 오류 페이지 판단 기준
        if "404" in page_source or "not found" in page_source:
            return "404 오류 - 페이지 없음"
        elif "this site can't be reached" in page_source or "ERR_NAME_NOT_RESOLVED" in page_source:
            return "접속 시간 초과 또는 도메인 비활성화"
        else:
            return "정상 페이지"
    except Exception as e:
        return f"알 수 없는 오류(Selenium): {e}"
    finally:
        driver.quit()

def check_url(url):
    # URL 앞에 http 또는 https 추가
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    # 1단계: HTTP 상태 코드 확인
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # 2단계: Selenium으로 추가 분석
            return check_url_with_selenium(url)
        elif response.status_code == 404:
            return "404 오류 - 페이지 없음"
        else:
            return f"HTTP 상태 코드 오류: {response.status_code}"
    except requests.exceptions.Timeout:
        return "오류 - 접속 시간 초과"
    except requests.exceptions.ConnectionError:
        return "오류 - 도메인 비활성화"
    except Exception as e:
        return f"알 수 없는 오류(Requests): {e}"

# 테스트
url_list = [
    "http://example.com",               # 정상 URL
    "adpartner.or.kr",    # 접속 불가 URL
    "http://adpbc.or.kr",           # 404 오류 페이지
]

for url in url_list:
    print(f"URL: {url} -> 결과: {check_url(url)}")
