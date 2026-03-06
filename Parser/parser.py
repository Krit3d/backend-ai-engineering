from bs4 import BeautifulSoup
import requests

url = "https://news.ycombinator.com/"
r = requests.get(url)

# Превращаем сырой HTML-текст в объект BeautifulSoup, с которым удобно работать
soup = BeautifulSoup(r.text, "html.parser")

# Выбираем все теги <a> по css-селектору.
# Аналогично можно сделать при помощи .find_all()
news_titles = soup.select(".titleline > a")
# Выводим текст(заголовок) у каждого тега(новости)
for t in news_titles:
    print(t.text, end="\n")