import requests
from bs4 import BeautifulSoup

def parse_website(url: str, dyn: bool) -> str:
    if dyn is True:
        url += "?ajax=true"
        result = requests.get(url)
        return result.json()
    else:
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "html.parser")
        # for script in soup(["script", "style"]):
        #     script.extract()
        return soup.prettify()