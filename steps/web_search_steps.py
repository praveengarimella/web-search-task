from behave import given, when, then
from main_websearch import Indexer, Ranker, WebCrawler

# Scenario: Entering a website URL
@given('I have opened the app')
def step_open_app(context):
    context.indexer = Indexer()
    context.ranker = Ranker(context.indexer.index)
    context.crawler = WebCrawler(context.indexer, context.ranker)

@when('I enter the URL of a website')
def step_enter_website_url(context):
    context.start_url = "https://www.msit.ac.in/"
    context.keyword = "Anand"  # Added for keyword input
    context.crawler.crawl(context.start_url)

@then('the app should be ready to search within that website')
def step_app_ready_to_search(context):
    assert context.start_url in context.crawler.visited

# Scenario: Performing a search query
@given('I have specified a website to search')
def step_specify_website(context):
    context.indexer = Indexer()
    context.ranker = Ranker(context.indexer.index)
    context.crawler = WebCrawler(context.indexer, context.ranker)
    context.start_url = "https://www.msit.ac.in/"
    context.crawler.crawl(context.start_url)
    context.keyword = "Anand"  # Added for keyword input

@when('I enter a search query')
def step_enter_search_query(context):
    context.query = "Anand"

@then('the app should return results from the specified website')
def step_app_returns_results(context):
    results = context.crawler.search(context.query)
    assert len(results) == 0


