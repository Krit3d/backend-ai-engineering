import requests
from random import choice
from time import sleep


def get_actual_price(coin=None, currency="usd"):
    if coin is None:
        coin = {"id": "bitcoin", "name": "Bitcoin"}

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin['id']}&vs_currencies={currency}"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        # В случае исключения сообщаем об этом пользователю
        print(f"Your request returned an exception: {type(e).__name__}.")
        print("Please check your internet connection")
    else:
        if response.status_code == 200:
            # Превращаем JSON-ответ в словарь Python
            data = response.json()

            # Возваращаем искомую цену
            return f"The current value of 1 {coin['name']} is {data.get(coin['id'], {}).get(currency, 'No data')} {currency.upper()}."

        return "Server Error. Please wait or check if your request is right"


# Список всех монет
COINS_LIST = requests.get("https://api.coingecko.com/api/v3/coins/list").json()
# Делаем задержку между запросами(хотя она тут не особо поможет :))
sleep(1)
# Список котируемых валют
COUNTER_CURRENCIES = requests.get(
    "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
).json()

print(get_actual_price(choice(COINS_LIST), choice(COUNTER_CURRENCIES)))
sleep(1)
print(get_actual_price(choice(COINS_LIST), choice(COUNTER_CURRENCIES)))
sleep(1)
print(get_actual_price(choice(COINS_LIST), choice(COUNTER_CURRENCIES)))
