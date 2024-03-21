from flask import Flask, request, jsonify
from main_websearch import Indexer, Ranker, WebCrawler

app = Flask(__name__)
indexer = Indexer()
ranker = Ranker(indexer.index)
crawler = WebCrawler(indexer, ranker)

@app.route('/')
def index():
    return 'Welcome to the Web Search API!'
@app.route('/index_page', methods=['POST'])
def index_page():
    data = request.json
    url = data.get('url')
    text_content = data.get('text_content')

    if not url or not text_content:
        return jsonify({'error': 'Both URL and text_content are required.'}), 400

    indexer.index_page(url, text_content)
    return jsonify({'message': 'Page indexed successfully.'}), 200

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

@app.route('/rank', methods=['GET'])
def rank():
    try:
        ranked_index = ranker.rank_index()
        return jsonify({"ranked_index": ranked_index})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)