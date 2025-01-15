#request로만 확인하기

import pandas as pd
import requests

def check_url(url):
    """도메인 비활성화 및 교회 단어 탐지"""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # URL에 http:// 추가

    try:
        # HEAD 요청으로 도메인 비활성화 확인
        response = requests.get(url, timeout=5, allow_redirects=True)
        print("테스트 내용: ")
        print(response.text)
        # 페이지 내용에서 "교회" 단어 탐지
        if response.status_code == 200:
            if "교회" in response.text:
                return "교회 발견"
            return ""  # 정상 페이지에서 "교회" 미발견 시 빈칸 출력

        return "도메인 비활성화" if response.status_code >= 400 else ""

    except requests.exceptions.ConnectionError:
        return "도메인 비활성화"
    except requests.exceptions.Timeout:
        return "도메인 비활성화"
    except Exception:
        return ""  # 기타 오류는 빈칸 출력

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
        
        # 결과가 빈칸이 아니면 "장인환" 추가
        entry = {"URL": link, "결과": result}
        if result:
            entry["추가"] = "장인환"
        results.append(entry)

    # 결과를 엑셀 파일로 저장
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_path, index=False)
    print(f"결과가 저장되었습니다: {output_path}")

# 테스트: 파일 경로 설정
input_file = "C:/Users/user/Desktop/2025 KISA/테스트 폴더/input.xlsx"  # 입력 파일 경로
output_file = "C:/Users/user/Desktop/2025 KISA/테스트 폴더/output.xlsx"  # 결과 저장 경로

process_links_from_excel(input_file, output_file)
