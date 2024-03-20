from flask import Flask, request, jsonify
from main_websearch import Indexer, Ranker, WebCrawler

app = Flask(__name__)
indexer = Indexer()
ranker = Ranker(indexer.index)
crawler = WebCrawler(indexer, ranker)

@app.route('/')
def index():
    return 'Welcome to the Web Search API!'

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    start_url = data.get('start_url')
    if not start_url:
        return jsonify({"error": "Start URL is required"}), 400
    crawler.crawl(start_url)
    return jsonify({"message": "Crawling completed successfully!"})

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url')
    keyword = request.args.get('keyword')

    # Perform crawling on the specified URL
    crawler.crawl(url)

    # Search for the keyword in the crawled content
    results = crawler.search(keyword)

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
