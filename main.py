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
            if keyword.lower() in text.lower(): #Here it was written not in it was changed to in because when we write not in then it will never add into results list. To fix it we add all the words which are in them and add all to results list.   
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(result) #changed undefined variables to result
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url) # changed craw to crawl, # function calling is fixed

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
