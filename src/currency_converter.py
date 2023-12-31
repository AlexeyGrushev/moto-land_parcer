import requests


def rub_to_byn(amount):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    rub_to_byn_rate = data['Valute']['BYN']['Value']
    return round((amount / rub_to_byn_rate * 1.3), 0)
