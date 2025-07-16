from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime, timedelta

# Chrome WebDriver 자동 설치
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"WebDriver 설치 및 실행 오류: {e}")
    exit()

# 데이터를 누적할 리스트를 미리 선언
all_news_data = []

# 크롤링할 날짜 범위 설정 (오늘부터 30일 전까지)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# 날짜별로 루프 실행
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y%m%d')
    url = f"https://news.naver.com/breakingnews/section/101/258?date={date_str}"

    print(f"\n### 날짜: {date_str} 기사 크롤링 시작 ###")
    driver.get(url)
    time.sleep(2)

    # '기사 더보기' 버튼이 사라질 때까지 클릭하는 루프
    while True:
        try:
            more_button = driver.find_element(By.CLASS_NAME, 'section_more_inner')
            more_button.click()
            time.sleep(1)
        except Exception:
            print("더 이상 '더보기' 버튼이 없습니다. 다음 날짜로 넘어갑니다.")
            break

    # 모든 기사가 로딩된 후, BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news_items = soup.find_all('li', class_='sa_item')

    if not news_items:
        print("뉴스 기사를 찾을 수 없습니다.")
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

    # 다음 날짜로 이동
    current_date += timedelta(days=1)

# 모든 크롤링이 끝난 후 CSV 파일로 저장
file_name = 'naver_news_one_month.csv'
fields = ['날짜', '제목', '링크']

if all_news_data:
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_news_data)
    print(f"\n총 {len(all_news_data)}개의 기사를 {file_name} 파일에 저장했습니다.")
else:
    print("저장할 기사가 없습니다.")

# 브라우저 닫기
driver.quit()