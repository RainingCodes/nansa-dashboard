import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 1. 데이터 읽기
df = pd.read_csv('data/naver_news_one_month.csv', names=['날짜', '제목', '링크'])

# 2. 회사명 리스트
company_list = ['삼성', '현대', '네이버', '카카오', 'LG', 'SK', '한화', '롯데']

# 3. 제목에 회사명 포함된 행만 필터링
def find_company(title):
    for company in company_list:
        if company in title:
            return company
    return None

df['회사명'] = df['제목'].apply(find_company)
filtered_df = df.dropna(subset=['회사명'])

# 4. 워드카운트 딕셔너리 만들기 (회사명 빈도)
company_counts = filtered_df['회사명'].value_counts().to_dict()

# 5. 워드클라우드 생성 및 시각화

font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path, size=15)
wc = WordCloud(font_path=font_path, background_color='white', width=800, height=400)
plt.figure(figsize=(10,5))
plt.title('한 달 간 뉴스 제목에 등장한 회사명 워드클라우드', fontproperties=font_prop)
plt.imshow(wc.generate_from_frequencies(company_counts))
plt.axis('off')
plt.savefig('plot/wordcloud_companies_name.png', bbox_inches='tight')
