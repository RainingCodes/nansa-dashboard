import os
import re
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from ksenticnet_kaist import ksenticnet

# ===== 0. 기본 설정 ===== #
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path, size=15)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name

# ===== 1. 데이터 불러오기 및 기업 매핑 ===== #
df = pd.read_csv('data/naver_news_one_month.csv', names=['날짜', '제목', '링크'])

# 기업 리스트와 alias 설정 (너가 주신 그대로 삽입)
company_list = [
    '삼성전자',               # 삼성
    'SK하이닉스',            # SK
    '삼성바이오로직스',       # 삼성
    'LG에너지솔루션',         # LG
    '삼성전자우',            # 삼성
    'KB금융',                # 기타 (금융)
    '한화에어로스페이스',      # 한화
    '현대차',                # 현대
    '두산에너빌리티',         # 두산
    '셀트리온',              # 기타 (바이오)
    '기아',                 # 현대
    'NAVER',               # 네이버
    'HD현대중공업',          # 현대
    '신한지주',              # 기타 (금융)
    '삼성물산',              # 삼성
    '현대모비스',            # 현대
    '삼성생명',              # 삼성
    '알테오젠',              # 기타 (바이오)
    '하나금융지주',           # 기타 (금융)
    'HMM',                 # 기타 (해운)
    '카카오',               # 카카오
    'POSCO홀딩스',           # 기타 (포스코)
    '한화오션',              # 한화
    'HD한국조선해양',         # 현대
    '한국전력',              # 기타 (공기업)
    '삼성화재',              # 삼성
    '현대로템',              # 현대
    'SK스퀘어',              # SK
    '메리츠금융지주',         # 기타 (금융)
    'LG화학',               # LG
    '우리금융지주',           # 기타 (금융)
    'KT&G',               # 기타 (담배)
    'HD현대일렉트릭',        # 현대
    'SK이노베이션',          # SK
    '기업은행',              # 기타 (금융/공기업)
    '크래프톤',              # 기타 (게임)
    '고려아연',              # 기타 (소재)
    '삼성중공업',            # 삼성
    'SK',                  # SK
    '삼성에스디에스',         # 삼성
    'KT',                  # 기타 (통신)
    '삼성SDI',              # 삼성
    '카카오뱅크',            # 카카오
    'LIG넥스원',             # 기타 (방산)
    'LG',                  # LG
    'LG전자',               # LG
    'SK텔레콤',             # SK
    '미래에셋증권',           # 기타 (금융)
    '하이브',                # 기타 (엔터)
    '삼양식품'               # 기타 (식품)
]
company_aliases = {
    '삼성전자우': ['삼성전자우', '삼성 전자우', '삼성전자 우선주', '삼성전자', '삼성 전자', 'Samsung Electronics'],
    '삼성전자': ['삼성전자', '삼성 전자', 'Samsung Electronics'],
    'SK하이닉스': ['SK하이닉스', 'SK 하이닉스', '하이닉스'],
    '삼성바이오로직스': ['삼성바이오로직스', '삼성 바이오로직스'],
    'LG에너지솔루션': ['LG에너지솔루션', 'LG 에너지솔루션'],
    'KB금융': ['KB금융', 'KB 금융', 'KB'],
    '한화에어로스페이스': ['한화에어로스페이스', '한화 에어로스페이스'],
    '현대차': ['현대차', '현대 자동차', '현대자동차', '현대'],
    '기아': ['기아', '기아자동차', '기아 자동차'],
    'NAVER': ['NAVER', '네이버'],
    '두산에너빌리티': ['두산에너빌리티', '두산 에너빌리티'],
    '셀트리온': ['셀트리온'],
    'HD현대중공업': ['HD현대중공업', '현대중공업', 'HD 현대중공업'],
    '신한지주': ['신한지주', '신한 금융'],
    '삼성물산': ['삼성물산', '삼성 물산'],
    '현대모비스': ['현대모비스', '현대 모비스'],
    '삼성생명': ['삼성생명', '삼성 생명'],
    '알테오젠': ['알테오젠'],
    '하나금융지주': ['하나금융지주', '하나 금융'],
    'HMM': ['HMM'],
    '카카오': ['카카오'],
    'POSCO홀딩스': ['POSCO홀딩스', '포스코홀딩스', '포스코'],
    '한화오션': ['한화오션', '한화 오션'],
    'HD한국조선해양': ['HD한국조선해양', '한국조선해양'],
    '한국전력': ['한국전력', '한전'],
    '삼성화재': ['삼성화재', '삼성 화재'],
    '현대로템': ['현대로템', '현대 로템'],
    'SK스퀘어': ['SK스퀘어', 'SK 스퀘어'],
    '메리츠금융지주': ['메리츠금융지주', '메리츠 금융', '메리츠'],
    'LG화학': ['LG화학', 'LG 화학'],
    '우리금융지주': ['우리금융지주', '우리 금융'],
    'KT&G': ['KT&G', '케이티앤지'],
    'HD현대일렉트릭': ['HD현대일렉트릭', '현대일렉트릭'],
    'SK이노베이션': ['SK이노베이션', 'SK 이노베이션'],
    '기업은행': ['기업은행', 'IBK', '중소기업은행'],
    '크래프톤': ['크래프톤'],
    '고려아연': ['고려아연', '고려 아연'],
    '삼성중공업': ['삼성중공업', '삼성 중공업'],
    'SK': ['SK'],
    '삼성에스디에스': ['삼성에스디에스', '삼성 SDS'],
    'KT': ['KT'],
    '삼성SDI': ['삼성SDI', '삼성 SDI'],
    '카카오뱅크': ['카카오뱅크', '카카오 뱅크'],
    'LIG넥스원': ['LIG넥스원', 'LIG 넥스원'],
    'LG': ['LG'],
    'LG전자': ['LG전자', 'LG 전자'],
    'SK텔레콤': ['SK텔레콤', 'SK 텔레콤'],
    '미래에셋증권': ['미래에셋증권', '미래에셋', '미래 에셋'],
    '하이브': ['하이브', 'HYBE'],
    '삼양식품': ['삼양식품', '삼양 식품']
}

# ===== 2. 회사 탐색 함수 정의 ===== #
def find_companies(title):
    matched = set()
    for company, aliases in company_aliases.items():
        for alias in aliases:
            if re.search(rf'\b{re.escape(alias)}\b', title, re.IGNORECASE):
                matched.add(company)
    return list(matched)

df['회사목록'] = df['제목'].apply(find_companies)
filtered_df = df[df['회사목록'].map(len) > 0]

# ===== 3. 텍스트 전처리 및 감성 분석 ===== #
def tokenize(text):
    return re.findall(r'\b[가-힣]{2,}\b', text)

def get_sentiment(word):
    entry = ksenticnet.get(word)
    return entry[6] if entry else None

def load_sentiment_words(tokens):
    stopwords = ['뉴스', '관련', '보도', '기자']
    filtered = [w for w in tokens if w not in stopwords]
    word_freq = Counter(filtered)
    pos_words = {w for w in filtered if get_sentiment(w) == 'positive'}
    neg_words = {w for w in filtered if get_sentiment(w) == 'negative'}
    return word_freq, pos_words, neg_words

# ===== 4. 시각화 함수 정의 ===== #
def draw_wordcloud(word_freq, path, title, color_map='gray', color_func=None):
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        width=800, height=400
    )
    plt.figure(figsize=(10, 5))
    plt.title(title, fontproperties=font_prop)
    img = wc.generate_from_frequencies(word_freq)
    if color_func:
        img = wc.recolor(color_func=color_func)
    plt.imshow(img, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def draw_sentiment_pie(pos_count, neg_count, company):
    sizes = [pos_count, neg_count]
    labels = ['긍정', '부정']
    colors = ['skyblue', 'salmon']
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        startangle=90,
        labeldistance=1.2,
        autopct='%.1f%%',
        textprops={'fontsize': 12},
        pctdistance=0.7
    )
    ax.set_title(f'{company} 뉴스 감성 비율', fontproperties=font_prop)
    ax.axis('equal')
    plt.tight_layout()
    os.makedirs('plot/plots/posneg', exist_ok=True)
    plt.savefig(f'plot/plots/posneg/pie_posneg_{company}.png', bbox_inches='tight')
    plt.close()

# ===== 5. 회사별 뉴스 수집 및 시각화 ===== #
company_titles = {company: [] for company in company_list}

for _, row in filtered_df.iterrows():
    for company in row['회사목록']:
        if company in company_titles:
            company_titles[company].append(row['제목'])

for company, titles in company_titles.items():
    if not titles:
        print(f"[스킵] {company}: 관련 뉴스 없음")
        continue

    text = ' '.join(titles)
    tokens = tokenize(text)
    word_freq, pos_words, neg_words = load_sentiment_words(tokens)

    if not word_freq:
        print(f"[스킵] {company}: 유효한 키워드 없음")
        continue

    top_n = max(1, int(len(word_freq) * 0.1))
    top_words = dict(word_freq.most_common(top_n))

    os.makedirs('plot/plots/top10', exist_ok=True)
    os.makedirs('plot/plots/posneg', exist_ok=True)

    # 상위 키워드 워드클라우드
    draw_wordcloud(
        top_words,
        f'plot/plots/top10/wordcloud_headline_keyword_top10p_{company}.png',
        f'{company} 뉴스 상위 키워드'
    )

    # 긍정 단어
    if pos_words:
        pos_freq = {w: word_freq[w] for w in pos_words}
        draw_wordcloud(
            pos_freq,
            f'plot/plots/posneg/wordcloud_positive_{company}.png',
            f'{company} 긍정 단어',
            color_map='Blues'
        )

    # 부정 단어
    if neg_words:
        neg_freq = {w: word_freq[w] for w in neg_words}
        draw_wordcloud(
            neg_freq,
            f'plot/plots/posneg/wordcloud_negative_{company}.png',
            f'{company} 부정 단어',
            color_map='Reds'
        )

    # 감성 통합 색상 워드클라우드
    def sentiment_color_func(word, **kwargs):
        if word in pos_words:
            return 'blue'
        elif word in neg_words:
            return 'red'
        return 'gray'

    draw_wordcloud(
        top_words,
        f'plot/plots/posneg/wordcloud_sentiment_colored_{company}.png',
        f'{company} 감성 통합 워드클라우드',
        color_func=sentiment_color_func
    )

    # 파이차트
    total_pos = sum(word_freq[w] for w in pos_words)
    total_neg = sum(word_freq[w] for w in neg_words)
    if total_pos + total_neg > 0:
        draw_sentiment_pie(total_pos, total_neg, company)
