import string
import io
import unittest
from multiprocessing import Process
from random import randint, choices, normalvariate
import xmlrunner
from xmlrunner.extra.xunit_plugin import transform
from time import sleep
from server.app import start
from scraper import WebScraper

COMPANIES = [
    ("Quantum Dynamics Corp.", "QDY"),
    ("NexGen Solutions Inc.", "NGS"),
    ("Vertex Innovations Ltd.", "VTX"),
    ("Global Synergy Corp.", "GSC"),
    ("Aether Technologies", "ATH"),
    ("Zenith Power Systems", "ZPS"),
    ("Titanium Industries Inc.", "TII"),
    ("Blue Horizon Solutions", "BHS"),
    ("Pinnacle Ventures LLC", "PVL"),
    ("Solstice Pharmaceuticals", "SOL")
]

class TestWebScraper(unittest.TestCase):
    PORT = 5001

    name, ticker = choices(COMPANIES)[0]
    ytd_return = "{}%".format(round(normalvariate(10, 3), 1))
    price = round(normalvariate(100, 5))

    p = Process(target=start, args=(PORT, name, ticker, ytd_return, price))

    @classmethod
    def setUpClass(cls):        
        cls.p.start()
        sleep(2)

        cls.scraper = WebScraper(cls.PORT)
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.p.kill()

    def test_scrape_company_name(self):
        name = self.scraper.scrapeCompanyName()
        self.assertEqual(self.name, name)

    def test_scrape_company_ticker(self):
        ticker = self.scraper.scrapeCompanyTicker()
        self.assertEqual(self.ticker, ticker)

    def test_scrape_ytd_return(self):
        ytd_return = self.scraper.scrapeYtdReturn()
        self.assertEqual(self.ytd_return, ytd_return)

    def test_scrape_avg_close(self):
        avg_close = self.scraper.scrapeAvgClose()
        self.assertAlmostEqual(self.price, avg_close)


if __name__ == "__main__":
    with open('unit.xml', 'wb') as output:
        unittest.TestLoader.sortTestMethodsUsing = None
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
