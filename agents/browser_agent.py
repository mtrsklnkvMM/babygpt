from collections import deque
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from duckduckgo_search import ddg
from agents.scrapper_agent import ScrapperAgent


class BrowserAgent:
    def __init__(self, api_key, engine_id):
        self.api_key = api_key
        self.service = build('customsearch', 'v1', developerKey=api_key)
        self.fallback_service = ddg
        self.engine_id = engine_id
        self.used_urls = deque([])
     
    def strip_query(self, query):
        if isinstance(query, str):
            return query.replace('\\', ' ')
        elif isinstance(query, tuple):
            old_value, *rest = query
            return old_value.replace('\\', ' ')
    

    def browse_google(self, query, agent, num_results=10):
        try:
            stripped_query = self.strip_query(query)
            res = self.service.cse().list(q=stripped_query, cx=self.engine_id, num=num_results).execute()
            items = res.get('items', [])
            results = [(item.get('title', ''), item.get('link', '')) for item in items]

            r_string = json.dumps(results)
            reponse = agent.open_ai.generate_text(f"""We are trying to: {agent.active_task.expected_output}, 
            please return the most interesting url from that list: {r_string}, that is NOT in that list: {', '.join(str(e) for e in self.used_urls)}.
            Just return a simple string like: https://foo.com """)
            print(reponse)
            return [reponse]
        
        except HttpError as error:
            print(f'An error occurred while browsing Google: {error}')
            return []


    def browse_ddg(self, query, agent):
        try:
            stripped_query = self.strip_query(query)
            res = self.fallback_service(stripped_query, max_results = 10)
            results = [(item.get('title', ''), item.get('href', '')) for item in res]

            r_string = json.dumps(results)
            reponse = agent.open_ai.generate_text(f"""We are trying to: {agent.active_task.expected_output}, 
            please return the most interesting url from that list: {r_string}, that is NOT in that list: {', '.join(str(e) for e in self.used_urls)}.
            Just return a simple string like: https://foo.com """)
            print(reponse)
            return [reponse]
        
        except Exception as e:
            print(f'An error occurred while browsing DuckDuckGo: {e}')
            return []
        

    def browse(self, query, agent):
        try:
            return self.browse_google(query, agent)
        
        except HttpError as error:
            print(f'An error occurred while browsing Google: {error}')
            print('Fallback to DuckDuckGo')
            return self.browse_ddg(query, agent)


    def scrape(self, link):
        self.used_urls.append(link)
        scrapper = ScrapperAgent(link)
        return scrapper.scrape()


    def search(self, query, agent):
        results = self.browse(query, agent)
        scraped_data = []
        for result in results:
            link = result
            data = self.scrape(link)
            scraped_data.append(data)
        
        return scraped_data
    
    def searchDDG(self, query, agent):
        results = self.browse_ddg(query, agent)
        scraped_data = []
        for result in results:
            link = result
            data = self.scrape(link)
            scraped_data.append(data)
        
        return scraped_data