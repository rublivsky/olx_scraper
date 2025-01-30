import json
import aiohttp
import asyncio
from datetime import datetime as dt
from bs4 import BeautifulSoup

def format_datetime(dtime: str):
    months = {
        '01': 'січня', '02': 'лютого', '03': 'березня', '04': 'квітня',
        '05': 'травня', '06': 'червня', '07': 'липня', '08': 'серпня',
        '09': 'вересня', '10': 'жовтня', '11': 'листопада', '12': 'грудня'
    }
    if 'Сьогодні о ' in dtime:
        current_date = dt.now().strftime("%d-%m-%Y ").split('-')
        dtime = dtime.replace('Сьогодні о ', f'{current_date[0]} {months[current_date[1]]} {current_date[2]} р. ')
    elif 'Сегодня в ' in dtime:
        current_date = dt.now().strftime("%d-%m-%Y ").split('-')
        dtime = dtime.replace('Сегодня в', f'{current_date[0]} {months[current_date[1]]} {current_date[2]} р. ')
    return dtime

async def fetch(session, url: str):
    async with session.get(url) as response:
        # print(f"Status code: {response.status}")
        return await response.text()

async def main():
    base_url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/q-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/?currency=UAH&page={page}&search%5Bdistrict_id%5D=115&search%5Bfilter_float_floor%3Afrom%5D=2&search%5Bfilter_float_price%3Afrom%5D=7000&search%5Bfilter_float_price%3Ato%5D=12500&search%5Bfilter_float_total_area%3Afrom%5D=30&search%5Bphotos%5D=1'
    publications = []
    
    async with aiohttp.ClientSession() as session:
        for page in range(1, 1000):
            url = base_url.format(page=page)
            html = await fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            
            items = soup.find_all('div', class_='css-l9drzq')
            if not items: break
            
            for item in items:
                title = item.find('h4', class_='css-1sq4ur2').text.strip()
                price = item.find('p', class_='css-6j1qjp').text.strip()
                date_publ = str(format_datetime(item.find('p', class_='css-1mwdrlh').text.strip().replace('Дніпро, Соборний - ', '')))
                url = item.find('div', class_='css-u2ayx9').find('a', class_='css-qo0cxu').get('href')
                url = (f'https://www.olx.ua/{url}')
                description = 0
                publications.append({
                    'title': title,
                    'price': price,
                    'date': date_publ,
                    'description': description,
                    'url': url
                })
                print(f'page: {page}\npublications: {len(publications)}')
    
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(publications, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: print('Bot stopped')