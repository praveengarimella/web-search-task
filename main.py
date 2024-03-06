import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
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
                    if urlparse(href).netloc:
                        href = urljoin(base_url or url, href)
                    if not href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            # Check if the lowercase version of the keyword 
            # is present in the lowercase version of the text.
            if keyword.lower()  in text.lower():   # here not is removed 
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                # Changed the usage of an undefined variable to 'result'
                # in the print_results method,
                print(f"- {result}")   # ensuring that each search result is printed correctly."
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    #  THE BUG IS FOUND HERE
    # crawler.craw(start_url)  This line contains bug. The name of the function is typed wrong.
    crawler.crawl(start_url)     # the bug is fixed. 

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
