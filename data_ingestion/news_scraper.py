import requests
from bs4 import BeautifulSoup

def scrape_bloomberg():
    url = "https://www.bloomberg.com/markets"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("h1")
    return [h.text for h in headlines]