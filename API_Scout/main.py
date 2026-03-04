import requests

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)

# Превращаем JSON-ответ в словарь Python
data = response.json()

# Выводим по ключу
print(f"Текущая стоимость 1 Биткоина($): {data["bitcoin"].get("usd")}")
