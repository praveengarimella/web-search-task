import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
from unittest.mock import MagicMock, patch, call

class WebCrawler:
    def __init__(self):
        # Index to store URL-text mapping
        self.index = defaultdict(list)
        # Set to keep track of visited URLs
        self.visited = set()

    def crawl(self, url, base_url=None):
        # Avoid unnecessary crawling if the URL has been visited
        if url in self.visited:
            return
        # Mark the current URL as visited
        self.visited.add(url)

        try:
            # Send HTTP GET request to the URL
            response = requests.get(url)
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Index the URL with its corresponding text content
            self.index[url] = soup.get_text()

            # Extract and crawl all anchor links ('a' tags) in the HTML
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    # Construct the new URL by joining the base_url and href
                    new_url = urljoin(base_url, href) if base_url else urljoin(url, href)
                    # Ensure the new URL is within the scope of the base_url or original URL
                    if new_url.startswith(url):
                        # Recursively crawl the new URL, considering the base_url if provided
                        self.crawl(new_url, base_url=base_url or url)
        except requests.exceptions.RequestException as e:
            # Raise a RequestException if there's an error during crawling
            raise requests.exceptions.RequestException(f"Error crawling {url}: {e}")

    def search(self, keyword):
        # Results list to store URLs containing the keyword
        results = []
        for url, text in self.index.items():
            # Check if the keyword is present in the text content
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")

def main():
    # Example usage of the WebCrawler class
    crawler = WebCrawler()
    start_url = "https://example.com"
    # Crawl the starting URL
    crawler.crawl(start_url)
    keyword = "test"
    # Search for the keyword in indexed content
    results = crawler.search(keyword)
    # Print the search results
    crawler.print_results(results)

import unittest

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get', side_effect=lambda url: MagicMock(text='<html><body><a href="/about">About Us</a></body></html>'))
    def test_crawl_success(self, mock_get):
        # Test a successful crawl operation
        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        # Assert that the visited URL is in the expected set
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get', side_effect=requests.exceptions.RequestException("Test Error"))
    def test_crawl_error(self, mock_get):
        # Test handling an error during the crawl
        crawler = WebCrawler()
        with self.assertRaises(requests.exceptions.RequestException):
            crawler.crawl("https://example.com")

    def test_search(self):
        # Test the search functionality
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No keyword here"
        results = crawler.search("keyword")
        # Assert that the search results match the expected set
        self.assertEqual(results, ["page1", "page2"])

    @patch('builtins.print')
    def test_print_results(self, mock_print):
        # Test printing search results
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        # Assert that the print function was called with the expected strings
        mock_print.assert_has_calls([
            call("Search results:"),
            call("- https://test.com/result")
        ])

if __name__ == "__main__":
    unittest.main()  # Run unit tests
    main()  # Run your main application logic