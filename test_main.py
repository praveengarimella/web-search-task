from main import WebCrawler
import unittest
from unittest.mock import patch, MagicMock, call
from urllib.parse import urljoin
import requests

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    # Verfies that the crawler correctly follows internal links found on a page and does not follow external links.
    def test_crawl_internal_links_success(self, mock_get):
        """Test crawling successfully follows internal links and ignores external links."""
        sample_html = """
        <html>
            <body>
                <h1>Welcome!</h1>
                <a href="/internal">Internal Link</a>
                <a href="http://external.com">External Link</a>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        base_url = "https://blogs.msit.ac.in/"
        crawler = WebCrawler()
        crawler.crawl(base_url)

        expected_url = urljoin(base_url, "/internal")
        self.assertIn(expected_url, crawler.visited)
        self.assertNotIn("http://external.com", crawler.visited)

    @patch('requests.get')
    def test_crawl_handles_request_exception(self, mock_get):
        # Tests the crawler's ability to gracefully handle exceptions during a request, such as network errors.
        """Test crawling gracefully handles request exceptions."""
        mock_get.side_effect = requests.exceptions.RequestException("Network Error")

        base_url = "https://blogs.msit.ac.in/error"
        crawler = WebCrawler()
        crawler.crawl(base_url)

        self.assertIn(base_url, crawler.visited)

    def test_search_finds_correct_urls(self):
        # Validates the search functionality by indexing two pages with distinct content—one containing a specified keyword ("framework") and the other not.
        """Test search function correctly identifies URLs containing the keyword."""
        crawler = WebCrawler()
        crawler.index = {
            "https://blogs.msit.ac.in/2024/02/07/mastering-the-machine-essential-tools-and-resources-for-it-professionals/": "This content contains the keyword framework.",
            "https://blogs.msit.ac.in/2024/02/14/soft-skills-for-tech-success-beyond-code-and-algorithms/": "This content does not contain the specific keyword."
        }

        results = crawler.search("framework")
        self.assertIn("https://blogs.msit.ac.in/2024/02/07/mastering-the-machine-essential-tools-and-resources-for-it-professionals/", results)
        self.assertNotIn("https://blogs.msit.ac.in/2024/02/14/soft-skills-for-tech-success-beyond-code-and-algorithms/", results)

    def test_search_case_insensitive(self):
        # Checks if the search function is case-insensitive
        """Test search function is case-insensitive."""
        crawler = WebCrawler()
        crawler.index = {
            "https://blogs.msit.ac.in/2024/01/08/ai-for-everyone-augmenting-our-minds-one-byte-at-a-time/": "Content with the KEYWORD in uppercase."
        }

        results = crawler.search("keyword")
        self.assertIn("https://blogs.msit.ac.in/2024/01/08/ai-for-everyone-augmenting-our-minds-one-byte-at-a-time/", results)

    def test_search_no_results_for_nonexistent_keyword(self):
        # Confirms that the search method returns no results when searching for a keyword that doesn't exist in any of the indexed content
        """Test search function returns no results for a nonexistent keyword."""
        crawler = WebCrawler()
        crawler.index = {
            "https://blogs.msit.ac.in/2024/01/08/ai-for-everyone-augmenting-our-minds-one-byte-at-a-time/": "This page does not contain the keyword."
        }

        results = crawler.search("nonexistent")
        self.assertEqual(len(results), 0)

    def test_search_with_empty_keyword_returns_no_results(self):
        # Ensures that searching with an empty keyword results in no matches found, which is the expected behavior for handling empty search queries.
        """Test search with an empty keyword returns no results."""
        crawler = WebCrawler()
        crawler.index = {
            "https://blogs.msit.ac.in/2024/02/07/mastering-the-machine-essential-tools-and-resources-for-it-professionals/": "This page contains some text."
        }

        results = crawler.search("")
        self.assertEqual(len(results), 0)

    @patch('sys.stdout')
    def test_print_results_correct_output(self, mock_stdout):
        # Captures and verifies the output of the print_results method to ensure it correctly displays the search results
        """Test print_results method prints the correct output."""
        crawler = WebCrawler()
        results = ["https://blogs.msit.ac.in/2024/01/08/ai-for-everyone-augmenting-our-minds-one-byte-at-a-time/"]
        crawler.print_results(results)

        # Adjusted expected_calls to match the actual output pattern
        expected_calls = [
            call('Search results:'),
            call('\n'),
            call('- https://blogs.msit.ac.in/2024/01/08/ai-for-everyone-augmenting-our-minds-one-byte-at-a-time/'),
            call('\n')
        ]
        mock_stdout.write.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
