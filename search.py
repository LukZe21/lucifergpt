import requests
from bs4 import BeautifulSoup
import google_custom_search
import wikipedia
import readability

class NotFound(Exception):
    pass

g_api_key = # your api key

google = google_custom_search.CustomSearch(apikey=g_api_key, engine_id="a3b37860c1cdc444e")

def google_search(query):
    readable_content = ''
    results = google.search(query)[:3]
    for result in results:
        response = requests.get(result.url)

        soup = BeautifulSoup(response.text, 'html.parser')

        for result in soup.find_all('p'):
            readable_content += result.get_text() + ' '
        
    return readable_content

def wikipedia_search(query):
    try:
        paragraphs = []
        search_result = wikipedia.search(query)[0]
        url = f"https://en.wikipedia.org/wiki/{search_result}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        for content in soup.find_all('p'):
            paragraphs.append(content.get_text())
        
        joined_paragarphs = ' '.join(paragraphs)
        
        if 'Other reasons this message may be displayed:' in joined_paragarphs:
            raise NotFound
        return joined_paragarphs
    except:
        return google_search(query)
