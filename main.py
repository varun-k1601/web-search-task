import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    href = urljoin(base_url or url, href)
                    if href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
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
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

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
        crawler.index["page2"] = "No match here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    def test_search_empty_index(self):
        crawler = WebCrawler()
        results = crawler.search("anything")
        self.assertEqual(results, [])

    def test_search_empty_keyword(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "Some content"
        results = crawler.search("")
        self.assertEqual(results, ["page1"])

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])

        # Assert that the output was captured correctly by mock_stdout

    def test_crawl_already_visited(self):
        crawler = WebCrawler()
        crawler.visited.add("https://example.com")
        with patch('requests.get') as mock_get:
            crawler.crawl("https://example.com")
            mock_get.assert_not_called()

    def test_print_results_no_results(self):
        crawler = WebCrawler()
        with patch('builtins.print') as mock_print:
            crawler.print_results([])
            mock_print.assert_any_call("No results found.")

    def test_print_results_multiple(self):
        crawler = WebCrawler()
        with patch('builtins.print') as mock_print:
            crawler.print_results(["url1", "url2"])
            mock_print.assert_any_call("Search results:")
            mock_print.assert_any_call("- url1")
            mock_print.assert_any_call("- url2")

if __name__ == "__main__":
    unittest.main()  # Run unit tests
    main()  # Run your main application logic
