import requests
from bs4 import BeautifulSoup

def get_financial_indices():
    """
    주요 경제 지표(KOSPI, KOSDAQ, USD/KRW 환율, NASDAQ)를 네이버 금융 웹사이트에서 크롤링하여 반환합니다.

    크롤링 대상:
    - KOSPI, KOSDAQ 지수: https://finance.naver.com/sise/
    - USD/KRW 환율: https://finance.naver.com/marketindex/
    - NASDAQ 지수: https://finance.naver.com/world/

    Returns:
        dict: 다음과 같은 키를 가지는 딕셔너리
            {
                'KOSPI': str,      # 예: '2,860.45'
                'KOSDAQ': str,     # 예: '902.32'
                'USD/KRW': str,    # 예: '1,396.50'
                'NASDAQ': str      # 예: '17,682.30'
            }

    Notes:
        - 웹 페이지 구조가 변경되면 동작하지 않을 수 있습니다.
        - 요청 실패 또는 파싱 실패 시, 해당 항목은 생략되고 오류 메시지가 출력됩니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    data = {}

    # 1. KOSPI, KOSDAQ
    try:
        sise_url = 'https://finance.naver.com/sise/'
        res = requests.get(sise_url, headers=headers)
        res.encoding = 'euc-kr'
        soup = BeautifulSoup(res.text, 'html.parser')

        kospi = soup.select_one('#KOSPI_now').text.strip()
        kosdaq = soup.select_one('#KOSDAQ_now').text.strip()

        data['KOSPI'] = kospi
        data['KOSDAQ'] = kosdaq
    except Exception as e:
        print(f"KOSPI/KOSDAQ 파싱 오류: {e}")

    # 2. USD/KRW
    try:
        fx_url = 'https://finance.naver.com/marketindex/'
        res = requests.get(fx_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        usdkrw = soup.select_one('div.head_info > span.value').text.strip()
        data['USD/KRW'] = usdkrw
    except Exception as e:
        print(f"USD/KRW 파싱 오류: {e}")

    # 3. NASDAQ
    try:
        world_url = 'https://finance.naver.com/world/'
        res = requests.get(world_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        nasdaq = soup.select_one('#worldIndexColumn2 > li.on > dl > dd.point_status > strong').text.strip()
        data['NASDAQ'] = nasdaq
    except Exception as e:
        print(f"NASDAQ 파싱 오류: {e}")

    return data


if __name__ == '__main__':
    x = get_financial_indices()
    print(x)

    