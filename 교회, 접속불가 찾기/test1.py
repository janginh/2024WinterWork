import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# URL 확인 함수
def check_url_with_selenium(url):
    # http:// 또는 https://로 시작하지 않으면 추가
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    options = Options()
    options.add_argument("--headless")  # 브라우저 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        print(f"Trying to open URL: {url}")
        driver.get(url)

        # 페이지가 로드될 때까지 기다리기
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # 페이지 소스에서 "교회"라는 단어 찾기
        page_source = driver.page_source.lower()
        if "this site can't be reached" in page_source or "err_name_not_resolved" in page_source:
            return "접속불가"
        elif "교회" in page_source:
            return "교회 발견"
        
        else:
            return ""
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return ""
    finally:
        driver.quit()

# 엑셀 파일 처리 함수
def process_links_from_excel(input_file, output_file):
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"엑셀 파일 읽기 오류: {str(e)}")
        return

    # A열의 링크 가져오기
    links = df.iloc[:, 0].dropna().tolist()

    results = []  # 결과 저장 리스트

    for link in links:
        print(f"Checking URL: {link}")
        result = check_url_with_selenium(link)  # URL 검사
        print(f"URL: {link} -> 결과: {result}")
        
        # 결과 저장
        '''result_dict = {"URL": link, "결과": result}
        if result == "교회발견" and result == "접속불가":
            result_dict["추가"] = "장인환"
        results.append(result_dict)'''
        
        if result:
            results.append({"URL": link, "결과": result, "추가": "장인환"})
        else:
            results.append({"URL": link, "결과": result})  # 결과가 빈칸일 경우 "장인환" 추가 안함


    # 결과를 엑셀 파일로 저장
    try:
        result_df = pd.DataFrame(results)
        result_df.to_excel(output_file, index=False)
        print(f"결과가 저장되었습니다: {output_file}")
    except Exception as e:
        print(f"엑셀 파일 저장 오류: {str(e)}")

# 테스트: 파일 경로 설정
input_file = "C:/Users/user/Desktop/2025 KISA/테스트 폴더/input.xlsx"  # 입력 파일 경로
output_file = "C:/Users/user/Desktop/2025 KISA/테스트 폴더/output.xlsx"  # 출력 파일 경로

process_links_from_excel(input_file, output_file)
