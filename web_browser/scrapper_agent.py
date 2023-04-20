import json
import re
import requests
from bs4 import BeautifulSoup


class ScrapperAgent:
    def __init__(self, url):
        self.url = url
        
    def scrape(self):
        # Send request
        try:
            response = requests.get(self.url, timeout=10)
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text
            text = soup.get_text()
            
            # Extract text and clean it
            text = soup.get_text()
            text = re.sub(r'[^\w\s]', '', text)  # remove non-alphanumeric characters
            text = re.sub(r'\s+', ' ', text)  # replace multiple whitespace with single space
            
            # Convert text to dictionary
            result_dict = {'text': text}
            json_string = json.dumps(result_dict)
            
            return json_string
        except requests.exceptions.Timeout:
            return 'Request timed out'
        except:
            return 'Error scraping website'