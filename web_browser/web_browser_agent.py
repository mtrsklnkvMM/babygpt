from collections import deque
from web_browser.result_summarizer_agent import ResultSummarizerAgent



class WebBrowserAgent:
    def __init__(self):
        self.used_keywords = deque([])
        self.used_urls = deque([])
        self.summarizer = ResultSummarizerAgent()
    


    def check_for_google(self, text):
        words = text.split()
        if "GOOGLE" in words:
            return True
        else:
            return False
    


    def get_keyword_prompt(self, task: str):
        prompt = f"""You are a Google Agent. This is the task: {task}, please return a relevant google query for google engine (4 keywords max)"""

        if self.used_keywords:
            message = f" (Note: Don't use these queries: {' or '.join(self.used_keywords)})"
            return prompt + message + " Keywords:"
        else:
            return prompt + " Keywords:"



    def get_analysis_prompt(self, summary: str, task: str):
        prompt = f"""My google search gave me the following result: '{summary}'.
            I was trying to solve the following problem: '{task}'.
            Did I get the information I wanted?. 

            If yes extract and return the important information from the result.

            If no just write 'GOOGLE' and I will try again. """
        return prompt
    


    def google(self, task: str, agent, retry = 0) -> str:
        
        agent.logger.log(f"Keyword Prompt: {task}")

        query = agent.open_ai.generate_text(task, 0.1)
        agent.logger.log(f"Keywords: {query}")

        self.used_keywords.append(query)

        scraped_data = agent.browser.get_from_internet(query, self.used_urls)
        summary = self.summarizer.summarize(scraped_data, agent)

        agent.logger.log(f"Summary: {summary}")

        memory_prompt = self.get_analysis_prompt(summary, task)

        agent.logger.log(f"Memory Prompt: {memory_prompt}")
        
        memory = agent.open_ai.generate_text(memory_prompt, 0.1)

        agent.logger.log(f"Memory: {memory}")

        if self.check_for_google(memory) and retry < 3:
            k = self.get_keyword_prompt(task)
            return self.google(task, agent, retry + 1)
        else:
            self.used_urls = []
            self.used_keywords = []
            return memory
