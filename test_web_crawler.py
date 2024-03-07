from main import WebCrawler
import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assert that 'about' was added to visited URLs
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assertions to check if the error was logged (you'll
        # likely need to set up logging capture in your tests)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1","page2"]) #added two pages. # here it was kept only one page

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])

        # Assert that the output was captured correctly by mock_stdout

if __name__ == "__main__":
    unittest.main()  # Run unit tests
