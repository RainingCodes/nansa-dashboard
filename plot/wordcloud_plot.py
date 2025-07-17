import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np


df = pd.read_csv('data/naver_news_one_month.csv', names=['날짜', '제목', '링크'])


company_list = ['삼성', '현대', '네이버', '카카오', 'LG', 'SK', '한화', '롯데']


def find_company(title):
    for company in company_list:
        if company in title:
            return company
    return None

df['회사명'] = df['제목'].apply(find_company)
filtered_df = df.dropna(subset=['회사명'])


company_counts = filtered_df['회사명'].value_counts().to_dict()


font_path = 'C:/Windows/Fonts/malgun.ttf'
font_prop = fm.FontProperties(fname=font_path, size=15)
font_name = fm.FontProperties(fname=font_path).get_name()
# matplotlib 전역 한글 폰트 설정
plt.rcParams['font.family'] = font_name


company_titles = {company: [] for company in company_list}


for _, row in filtered_df.iterrows():
    company = row['회사명']
    title = row['제목']
    company_titles[company].append(title)


from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from ksenticnet_kaist import ksenticnet

def tokenize(text):
    return re.findall(r'\b[가-힣]{2,}\b', text)  

def get_sentiment(word):
    entry = ksenticnet.get(word)
    if entry:
        return entry[6]  # 7번째 요소에 'positive' 또는 'negative'
    return None



for company, titles in company_titles.items():
    text = ' '.join(titles)
    tokens = tokenize(text)
    
    stopwords = [company, '뉴스', '관련', '보도', '기자']
    tokens = [word for word in tokens if company not in word and word not in ['뉴스', '관련', '보도', '기자']]

    word_freq = Counter(tokens)

    pos_words = {word for word in tokens if get_sentiment(word) == 'positive'}
    neg_words = {word for word in tokens if get_sentiment(word) == 'negative'}

    top_n = max(1, int(len(word_freq) * 0.1))
    top_words = dict(word_freq.most_common(top_n))

    # 1. 상위 단어 워드클라우드
    wc = WordCloud(font_path=font_path, background_color='white', width=800, height=400, margin=10)
    plt.figure(figsize=(10, 5))
    plt.title(f'{company} 관련 뉴스 제목 워드클라우드 (상위 10%)', fontproperties=font_prop)
    plt.imshow(wc.generate_from_frequencies(top_words))
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'plot/plots/top10/wordcloud_headline_keyword_top10p_{company}.png', bbox_inches='tight')

    # 2. 감성 단어 분리 빈도
    pos_freq = {word: word_freq[word] for word in pos_words}
    neg_freq = {word: word_freq[word] for word in neg_words}
    top_pos = Counter(pos_freq).most_common(10)
    top_neg = Counter(neg_freq).most_common(10)

    
    # 4. 긍정 워드클라우드
    if pos_freq:
        wc_pos = WordCloud(font_path=font_path, background_color='white', width=800, height=400, colormap='Blues')
        plt.figure(figsize=(10, 5))
        plt.title(f'{company} 긍정 단어 워드클라우드', fontproperties=font_prop)
        plt.imshow(wc_pos.generate_from_frequencies(pos_freq))
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'plot/plots/posneg/wordcloud_positive_{company}.png', bbox_inches='tight')

    # 5. 부정 워드클라우드
    if neg_freq:
        wc_neg = WordCloud(font_path=font_path, background_color='white', width=800, height=400, colormap='Reds')
        plt.figure(figsize=(10, 5))
        plt.title(f'{company} 부정 단어 워드클라우드', fontproperties=font_prop)
        plt.imshow(wc_neg.generate_from_frequencies(neg_freq))
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'plot/plots/posneg/wordcloud_negative_{company}.png', bbox_inches='tight')

    # 6. 감성 통합 색상 워드클라우드
    def color_func(word, **kwargs):
        if word in pos_words:
            return 'blue'
        elif word in neg_words:
            return 'red'
        else:
            return 'gray'

    wc_all = WordCloud(font_path=font_path, background_color='white', width=800, height=400)
    plt.figure(figsize=(10, 5))
    plt.title(f'{company} 감성 통합 워드클라우드', fontproperties=font_prop)

    img = wc_all.generate_from_frequencies(top_words)
    img = wc_all.recolor(color_func=color_func)

    plt.imshow(img, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'plot/plots/posneg/wordcloud_sentiment_colored_{company}.png', bbox_inches='tight')

    # 7. 감성 비율 파이 차트 (긍정 vs 부정만)
    total_pos = sum(pos_freq.values())
    total_neg = sum(neg_freq.values())

    labels = ['긍정', '부정']
    sizes = [total_pos, total_neg]
    colors = ['skyblue', 'salmon']

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
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
    plt.subplots_adjust(top=0.88)
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig(f'plot/plots/posneg/pie_posneg_{company}.png', bbox_inches='tight')






    
    
