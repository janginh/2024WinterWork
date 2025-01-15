import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

def check_url_with_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        page_source = driver.page_source.lower()
        # 접속 시간 초과 또는 도메인 비활성화 페이지 확인
        if "this site can't be reached" in page_source or "err_name_not_resolved" in page_source:
            return "접속 시간 초과 또는 도메인 비활성화"
        else:
            return ""  # 정상 페이지는 빈칸 출력
    except Exception as e:
        return ""  # 예외 처리: 정상적으로 페이지를 읽지 못한 경우 빈칸 출력
    finally:
        driver.quit()

def check_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # URL에 http:// 추가

    try:
        response = requests.get(url, timeout=10)
        
        # 도메인 비활성화는 requests로만 확인
        if response.status_code == 200:
            return ""  # 정상 페이지는 빈칸 출력
    except requests.exceptions.ConnectionError:
        return "접속불가"  # 도메인 비활성화 오류는 출력
    except Exception as e:
        return ""  # 나머지 예외는 빈칸 출력

def process_links_from_excel(file_path, output_path):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    
    # A열의 링크 가져오기
    links = df.iloc[:, 0].dropna().tolist()

    # 모든 링크 처리
    results = []
    for link in links:
        print(f"Checking URL: {link}")
        result = check_url(link)
        print(f"URL: {link} -> 결과: {result}")
        # 결과는 "장인환"만 추가
        results.append({"URL": link, "결과": result, "추가": "장인환"})  

    # 결과를 엑셀 파일로 저장
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_path, index=False)
    print(f"결과가 저장되었습니다: {output_path}")

# 테스트: 파일 경로 설정
input_file = "C:/Users/user/Desktop/2025 KISA/접속불가/input.xlsx"  # 입력 파일 경로 (A열에 URL이 포함된 엑셀 파일)
output_file = "C:/Users/user/Desktop/2025 KISA/접속불가/output.xlsx"  # 결과 저장 파일 경로

process_links_from_excel(input_file, output_file)
