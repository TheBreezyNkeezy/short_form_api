import requests
from bs4 import BeautifulSoup

def parse_website(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    return soup.prettify()
