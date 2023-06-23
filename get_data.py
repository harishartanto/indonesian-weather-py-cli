import re
import requests
from bs4 import BeautifulSoup as bs

URL = 'https://data.bmkg.go.id/prakiraan-cuaca/'

response = requests.get(URL)
html_page = bs(response.content, "html.parser")

all_links = html_page.find_all("a")

def get_province():
    province_url = {}
    for link in all_links:
        href = link['href']
        if href.startswith('../DataMKG/MEWS/DigitalForecast/DigitalForecast-'):
            province_url[link.text] = href
    return province_url

def data_cleaning(data):
    for key, value in list(data.items()):
        data[key] = value.replace('../', 'https://data.bmkg.go.id/')
        data[key.replace('DigitalForecast-', '').replace('.xml', '')] = data.pop(key)

    for key, value in list(data.items()):
        data[re.sub(r'([A-Z])(?=[A-Z][a-z])|([a-z])(?=[A-Z])', r'\1\2 ', key)] = data.pop(key)

    del data['Indonesia']

    return data

def data_filtering(data, filter_list):
    for key, _ in list(data.items()):
        if key not in filter_list:
            del data[key]
    return data