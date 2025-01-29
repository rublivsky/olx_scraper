import asyncio
import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/q-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/?search%5Bdistrict_id%5D=115&search%5Bphotos%5D=1&search%5Bfilter_float_price:from%5D=7000&search%5Bfilter_float_price:to%5D=12500&search%5Bfilter_float_floor:from%5D=2&search%5Bfilter_float_total_area:from%5D=30&currency=UAH'

async def main(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

if __name__ == '__main__':
   asyncio.run(main(url))