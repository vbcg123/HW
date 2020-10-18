import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.genie_top200

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

charts = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for chart in charts:
    rank = chart.select_one('td.number').text[0:2].strip()
    title = chart.select_one('td.info > a').text.strip()
    artist = chart.select_one('td.info > a.artist.ellipsis').text
    chart_data = {"rank": rank, "title": title, "artist": artist}
    db.charts.insert_one(chart_data)
    print(rank, title, "-", artist)
