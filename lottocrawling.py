import requests
from bs4 import BeautifulSoup
import json

# 특정 회차의 로또 데이터를 가져오는 함수
def get_lotto_data(round_number):
    url = f'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round_number}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for round {round_number}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 당첨 번호 크롤링
    try:
        win_numbers = [int(num.text) for num in soup.select('.num.win p span')]
        bonus_number = int(soup.select_one('.num.bonus p span').text)

        return {
            "round": round_number,
            "numbers": win_numbers,
            "bonus": bonus_number
        }
    except Exception as e:
        print(f"Error parsing data for round {round_number}: {e}")
        return None

# 최신 회차 번호를 가져오는 함수
def get_latest_round():
    url = 'https://dhlottery.co.kr/common.do?method=main'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    latest_round = int(soup.select_one('#lottoDrwNo').text)
    return latest_round

# 모든 회차의 데이터를 수집하여 리스트로 반환하는 함수
def get_all_lotto_data(start_round=1, end_round=None):
    all_data = []
    for round_number in range(start_round, end_round + 1):
        print(f"Fetching data for round {round_number}")
        data = get_lotto_data(round_number)
        if data:
            all_data.append(data)
    return all_data

# JSON 파일로 저장하는 함수
def save_to_json(data, filename="lotto_data.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# 최신 회차까지의 모든 데이터를 수집하여 JSON 파일로 저장
latest_round = get_latest_round()
all_lotto_data = get_all_lotto_data(1, latest_round)
save_to_json(all_lotto_data)
