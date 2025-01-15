#10개씩 읽어옴, 도메인 오류만 정확하게 확인 가능
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
        if "404" in page_source or "not found" in page_source:
            return "404 오류 - 페이지 없음"
        elif "this site can't be reached" in page_source or "err_name_not_resolved" in page_source:
            return "접속 시간 초과 또는 도메인 비활성화"
        else:
            return "정상 페이지"
    except Exception as e:
        return f"알 수 없는 오류(Selenium): {e}"
    finally:
        driver.quit()

def check_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
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

def process_links_from_excel(file_path, output_path):
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    
    # A열의 링크 가져오기
    links = df.iloc[:, 0].dropna().tolist()

    # 10개씩 나눠서 처리
    results = []
    for i in range(0, len(links), 10):
        batch = links[i:i + 10]
        print(f"Processing batch {i // 10 + 1}: {batch}")
        for link in batch:
            result = check_url(link)
            print(f"URL: {link} -> 결과: {result}")
            results.append({"URL": link, "결과": result})

    # 결과를 엑셀 파일로 저장
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_path, index=False)
    print(f"결과가 저장되었습니다: {output_path}")

# 테스트: 파일 경로 설정
input_file = "C:/Users/user/Desktop/2025 KISA/접속불가/input.xlsx"  # 입력 파일 경로 (A열에 URL이 포함된 엑셀 파일)
output_file = "C:/Users/user/Desktop/2025 KISA/접속불가/output.xlsx"  # 결과 저장 파일 경로
process_links_from_excel(input_file, output_file)
