from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
import requests

def check_url(url):
    # 1단계: HTTP 상태 코드 확인
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # 2단계: Selenium으로 추가 분석 (동적 오류 처리)
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
        return f"알 수 없는 오류: {e}"

# 테스트
url = "adpartner.or.kr"
print(check_url(url))
