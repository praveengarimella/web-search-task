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
                    if href.startswith(base_url or url): # removed not in this line of code because it has to crawl up when the url is matched
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower(): # removed not from this statement because the urls will not be appended into the list(results)
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}") # modified the code by changing the variable name which was causing the error.
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://www.youtube.com/" # changed the URL from example to msit
    crawler.crawl(start_url) #function calling is fixed.(spelling mistake fixed)

    keyword = "water" # Modified the key word
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
