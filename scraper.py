import json
import aiohttp
import asyncio
from datetime import datetime as dt
from bs4 import BeautifulSoup

url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/q-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/?search%5Bdistrict_id%5D=115&search%5Bphotos%5D=1&search%5Bfilter_float_price:from%5D=7000&search%5Bfilter_float_price:to%5D=12500&search%5Bfilter_float_floor:from%5D=2&search%5Bfilter_float_total_area:from%5D=30&currency=UAH'

def datetime(dtime: str):
    if 'Сьогодні о ' in dtime:
        months = {
            '01': 'січня', '02': 'лютого', '03': 'березня', '04': 'квітня',
            '05': 'травня', '06': 'червня', '07': 'липня', '08': 'серпня',
            '09': 'вересня', '10': 'жовтня', '11': 'листопада', '12': 'грудня'
        }
        current_date = dt.now().strftime("%d-%m-%Y ").split('-')
        dtime = dtime.replace('Сьогодні о ', f'{current_date[0]} {months[current_date[1]]} {current_date[2]} р. ')
    return dtime

async def fetch(session, url):
    async with session.get(url) as response:
        print(f"Status code: {response.status}")
        return await response.text()

async def main(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        publications = []
        for item in soup.find_all('div', class_='css-l9drzq'):
            title = item.find('h4', class_='css-1sq4ur2').text.strip()
            price = item.find('p', class_='css-6j1qjp').text.strip()
            date_publ = str(datetime(item.find('p', class_='css-1mwdrlh').text.strip().replace('Дніпро, Соборний - ', '')))
            url = item.find('div', class_='css-u2ayx9').find('a', class_='css-qo0cxu').get('href')
            publications.append({
                'title': title,
                'price': price,
                'date': date_publ,
                'url': url
            })

        with open('publications.json', 'w', encoding='utf-8') as f:
            json.dump(publications, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    asyncio.run(main(url))
