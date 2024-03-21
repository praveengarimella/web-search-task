from flask import Flask, request, jsonify
from main_websearch import Indexer, Ranker, WebCrawler

app = Flask(__name__)
indexer = Indexer()
ranker = Ranker(indexer.index)
crawler = WebCrawler(indexer, ranker)

@app.route('/')
def index():
    return 'Welcome to the Web Search API!'

@app.route('/index', methods=['POST'])
def index_page():
    data = request.json
    url = data.get('url')
    try:
        crawler.crawl(url)
        return jsonify({"message": "Page indexed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    start_url = data.get('start_url')
    if not start_url:
        return jsonify({"error": "Start URL is required"}), 400
    try:
        crawler.crawl(start_url)
        return jsonify({"message": "Crawling completed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url')
    keyword = request.args.get('keyword')

    if not url or not keyword:
        return jsonify({"error": "Both URL and keyword are required parameters."}), 400

    try:
        results = crawler.search(keyword)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
