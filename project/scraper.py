import requests
import json
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, port=5000) -> None:
        url = f"http://127.0.0.1:{port}"
        html = requests.get(url).text
        self.soup = BeautifulSoup(html, features="html.parser")

    def scrapeCompanyName(self) -> str:
        """Scrape the company name. For exaple, "Quantum Dynamics Corp.".
        """
        return self.soup.find('h1').string

    def scrapeCompanyTicker(self) -> str:
        """Scrape the company name. For exaple, "QDY".
        """
        return self.soup.select('.ticker')[0].string

    def scrapeYtdReturn(self) -> str:
        """Scrape the YTD return. For exaple, "12.3%".
        """
        tds = self.soup.select("#financial-data")[0].find_all('td')
        for i in range(len(tds) - 1):
            if tds[i].string == 'YTD Return':
                return tds[i+1].string

    def scrapeAvgClose(self) -> float:
        """Scrape the average closing price. For example, 129.0.
        """
        prices = json.loads(self.soup.find_all('script')[0].string)['ohlc']
        return sum([row['close'] for row in prices]) / len(prices)