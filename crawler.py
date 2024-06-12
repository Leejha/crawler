import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime

base_path = '/Users/junghyunkim/Google Drive/My Drive/wanted_notices'

# 결과 디렉토리가 없으면 생성
if not os.path.exists('./results'):
    os.makedirs('./results')

def print_with_time(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time}] {message}")

# 기본 경로 내의 각 폴더 순회 ex) 서울, 경기, 인천 등
for local_folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, local_folder)

    # 폴더가 맞는지 확인
    if os.path.isdir(folder_path):
        results_folder_path = os.path.join('/Users/junghyunkim/corp-reviews/crawler/results', local_folder)
        
        # 결과 디렉토리가 없으면 생성
        if not os.path.exists(results_folder_path):
            os.makedirs(results_folder_path)
        
        # 폴더 내의 각 csv 파일 순회
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # CSV 파일 읽기
                    df = pd.read_csv(file_path)

                    # 회사 위치를 저장할 새로운 열 추가
                    df['data-location'] = ''

                    # User-Agent 목록
                    user_agents = [
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                        # 추가 User-Agent 문자열들
                    ]

                    # 각 href 열의 URL을 방문하여 회사 위치 추출
                    for index, row in df.iterrows():
                        url = row['href']
                        headers = {'User-Agent': random.choice(user_agents)}
                        try:
                            response = requests.get(url, headers=headers, timeout=60)  # 타임아웃 설정
                            soup = BeautifulSoup(response.text, 'html.parser')

                            # 회사 위치가 포함된 HTML 요소 찾기 (예: <div class="company-location">)
                            location_tag = soup.find('span', class_='Typography_Typography__root__xYuMs Typography_Typography__body2__EpxWz Typography_Typography__weightMedium__O0Rdi')

                            if location_tag:
                                company_location = location_tag.get_text(strip=True)
                                df.at[index, 'data-location'] = company_location
                            else:
                                df.at[index, 'data-location'] = '위치 정보를 찾을 수 없습니다'

                            # 디버깅 메시지 출력
                            print_with_time(f"Index: {index}, URL: {url}, 회사 위치: {df.at[index, 'data-location']}")

                            # 랜덤 지연 시간 추가
                            time.sleep(random.uniform(1, 2))  # 1초에서 2초 사이의 랜덤 지연

                        except requests.exceptions.RequestException as e:
                            print_with_time(f"URL 요청 중 오류 발생: {url}, 오류: {e}")
                            df.at[index, 'data-location'] = '요청 중 오류 발생'

                    # 결과를 새로운 CSV 파일로 저장
                    result_file_path = os.path.join(results_folder_path, file_name)
                    df.to_csv(result_file_path, index=False)

                    # 파일이 제대로 저장되었는지 확인
                    print_with_time(f"CSV 파일이 '{result_file_path}'에 저장되었습니다.")

                except Exception as e:
                    print_with_time(f"파일 처리 중 오류 발생: {file_path}, 오류: {e}")