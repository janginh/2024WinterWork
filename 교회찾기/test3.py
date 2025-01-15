# 교회 발견은 잘하나 안열리는 경우가 다반수
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_url_with_selenium(url):
    print(f"Original URL: {url}")
    
    # http:// 또는 https://로 시작하지 않으면 추가
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url  # http:// 추가
    
    print(f"Final URL: {url}")  # 최종 URL 확인
    
    options = Options()
    options.add_argument("--headless")  # 최소 옵션으로 시작

    # ChromeDriver 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Trying to open URL...")
        driver.get(url)

        # 페이지 로딩 대기 시간 늘리기
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page loaded successfully.")

        page_source = driver.page_source.lower()  # 페이지 소스 가져오기
        if "교회" in page_source:
            return "교회 단어 발견"
        else:
            return "교회 단어 미발견"
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return f"오류 발생: {str(e)}"
    finally:
        driver.quit()

def process_links_from_excel(input_file, output_file):
    try:
        print(f"엑셀 파일 읽기 시도: {input_file}")
        df = pd.read_excel(input_file)
        print(f"엑셀 파일 읽기 성공: {input_file}")
    except Exception as e:
        print(f"엑셀 파일 읽기 오류: {str(e)}")
        return

    # A열의 링크 가져오기
    links = df.iloc[:, 0].dropna().tolist()

    if not links:
        print("엑셀 파일에 링크가 없습니다.")
        return

    # 결과를 저장할 리스트
    results = []

    # 각 URL에 대해 검사
    for link in links:
        print(f"Checking URL: {link}")
        result = check_url_with_selenium(link)  # '교회' 단어 찾기
        print(f"URL: {link} -> 결과: {result}")

        # 결과 저장
        results.append({"URL": link, "결과": result})

    try:
        print(f"결과 엑셀로 저장 중: {output_file}")
        result_df = pd.DataFrame(results)
        result_df.to_excel(output_file, index=False)
        print(f"결과가 저장되었습니다: {output_file}")
    except Exception as e:
        print(f"엑셀 파일 저장 오류: {str(e)}")

# 테스트: 파일 경로 설정
input_file = "C:/Users/user/Desktop/2025 KISA/교회찾기/input.xlsx"  # 실제 파일 경로로 변경
output_file = "C:/Users/user/Desktop/2025 KISA/교회찾기/output.xlsx"  # 실제 파일 경로로 변경

process_links_from_excel(input_file, output_file)
