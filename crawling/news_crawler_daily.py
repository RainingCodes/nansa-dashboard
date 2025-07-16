from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Chrome WebDriver 자동 설치
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"WebDriver 설치 및 실행 오류: {e}")
    exit()

# 명시적으로 날짜 지정
date_str = '20250716'
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
        print("더 이상 '더보기' 버튼이 없습니다. 크롤링을 종료합니다.")
        break

# 모든 기사가 로딩된 후, BeautifulSoup으로 HTML 파싱
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

# CSV 파일로 저장
if all_news_data:
    file_name = f'naver_news_{date_str}.csv'
    fields = ['날짜', '제목', '링크']
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_news_data)
    print(f"총 {len(all_news_data)}개의 기사를 {file_name} 파일에 저장했습니다.")
else:
    print("저장할 기사가 없습니다.")

# 브라우저 닫기
driver.quit()