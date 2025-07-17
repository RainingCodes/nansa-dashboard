from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options # Options 모듈 임포트
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime, timedelta
import os # 폴더 생성을 위해 os 모듈 임포트

# --- Chrome 옵션 설정 (헤드리스 모드 활성화) ---
chrome_options = Options()
chrome_options.add_argument("--headless") # GUI 없이 백그라운드에서 실행
chrome_options.add_argument("--no-sandbox") # 샌드박스 비활성화 (일부 환경에서 필요)
chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm 사용 비활성화 (리눅스 환경에서 메모리 문제 방지)
# 사용자 에이전트 설정 (봇으로 감지되는 것을 방지)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# --- 웹 드라이버 설정 ---
try:
    service = Service(ChromeDriverManager().install())
    # options 파라미터에 위에서 설정한 chrome_options 적용
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"WebDriver 설치 및 실행 오류: {e}")
    exit()

# --- 어제 날짜 계산 ---
# 현재 시간 기준 어제 날짜를 계산
today = datetime.now()
yesterday = today - timedelta(days=1)
date_str = yesterday.strftime('%Y%m%d')

# --- URL 설정 ---
url = f"https://news.naver.com/breakingnews/section/101/258?date={date_str}"

print(f"\n### 날짜: {date_str} 기사 크롤링 시작 (헤드리스 모드) ###")
driver.get(url)
time.sleep(2)

# --- '기사 더보기' 버튼 클릭 루프 ---
while True:
    try:
        more_button = driver.find_element(By.CLASS_NAME, 'section_more_inner')
        more_button.click()
        time.sleep(1) # 로딩 대기 시간
    except Exception:
        print("더 이상 '더보기' 버튼이 없습니다. 크롤링을 종료합니다.")
        break

# --- BeautifulSoup으로 HTML 파싱 및 데이터 추출 ---
soup = BeautifulSoup(driver.page_source, 'html.parser')
news_items = soup.find_all('li', class_='sa_item')

all_news_data = []
if not news_items:
    print("뉴스 기사를 찾을 수 없습니다. (빈 페이지 또는 구조 변경)")
else:
    for item in news_items:
        title_element = item.find('a', class_='sa_text_title')

        if title_element:
            try:
                link = title_element['href']
                title = title_element.find('strong').get_text(strip=True)
                all_news_data.append({
                    '날짜': date_str,
                    '제목': title,
                    '링크': link
                })
            except (KeyError, AttributeError):
                continue

# --- CSV 파일로 저장 ---
# 'daily' 폴더가 없으면 생성
output_folder = 'daily'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"'{output_folder}' 폴더를 생성했습니다.")

# 파일 경로 및 이름 설정: daily/YYYYMMDD.csv
file_name = f'{output_folder}/{date_str}.csv'
fields = ['날짜', '제목', '링크']

if all_news_data:
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_news_data)
    print(f"총 {len(all_news_data)}개의 기사를 {file_name} 파일에 저장했습니다.")
else:
    print("저장할 기사가 없습니다.")

# --- 브라우저 닫기 ---
driver.quit()