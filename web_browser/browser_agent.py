from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from duckduckgo_search import ddg
from web_browser.result_summarizer_agent import ResultSummarizerAgent
from web_browser.scrapper_agent import ScrapperAgent


class BrowserAgent:
    def __init__(self, api_key, engine_id):
        self.api_key = api_key
        self.service = build('customsearch', 'v1', developerKey=api_key)
        self.fallback_service = ddg
        self.engine_id = engine_id
        self.summarizer_helper = ResultSummarizerAgent()
     


    def scrape(self, link):
        scrapper = ScrapperAgent(link)
        return scrapper.scrape()



    def strip_query(self, query):
        if isinstance(query, str):
            return query.replace('\\', ' ')
        elif isinstance(query, tuple):
            old_value, *rest = query
            return old_value.replace('\\', ' ')



    def search_google(self, query, used_urls, num_results=10):
        try:
            stripped_query = self.strip_query(query)
            print(f"""3-{stripped_query}""")
            response = self.service.cse().list(q=stripped_query, cx=self.engine_id, num=num_results).execute()
            links = self.summarizer_helper.prioritize_links(response, stripped_query, used_urls)
            return links[:2]
        
        except HttpError as error:
            print(f'An error occurred while browsing Google: {error}')
            return []



    def search_ddg(self, query, used_urls):
        try:
            stripped_query = self.strip_query(query)
            data = self.fallback_service(stripped_query)
            links = [r['href'] for r in data]
            return links[:2]
        
        except Exception as e:
            print(f'An error occurred while browsing DuckDuckGo: {e}')
            return []



    def search_internet(self, query, used_urls = []):
        try:
            print(f"""2-{query}""")
            return self.search_google(query, used_urls)
        
        except HttpError as error:
            print(f'An error occurred while browsing Google: {error}')
            print('Fallback to DuckDuckGo')
            return self.search_ddg(query, used_urls)



    def get_from_internet(self, query, used_urls = []):
        print(f"""1-{query}""")
        results = self.search_internet(query, used_urls)
        scraped_data = []
        for result in results:
            link = result
            data = self.scrape(link)
            scraped_data.append(data)

        return " ".join(scraped_data)