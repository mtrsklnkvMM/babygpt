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
        prompt = f"""You are a Google Agent, helping me searching the google search engine. This is the task: {task}, please return the relevant google query as a string strictly:"""

        if self.used_keywords:
            message = f" (Note: Don't use these queries: {' or '.join(self.used_keywords)})"
            return prompt + message
        else:
            return prompt



    def get_analysis_prompt(self, summary: str, task: str):
        prompt = f"""My google search gave me the following result: '{summary}'.
            I was trying to solve the following problem: '{task}'.
            Did I get the information I wanted?. 
            If yes extract the important information from the result.
            If not just write 'GOOGLE' and I will try again. """
        return prompt
    


    def google(self, task: str, agent, retry = 0) -> str:
        prompt = self.get_keyword_prompt(task)
        agent.logger.log(f"Keyword Prompt: {prompt}")

        query = agent.open_ai.generate_text(prompt, 0.1)
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
            return self.google(task, agent, retry + 1)
        else:
            self.used_urls = []
            self.used_keywords = []
            return memory
