from agents.IAgent import AgentData
from web_browser.result_summarizer_agent import ResultSummarizerAgent



class WebBrowserAgent:
    def __init__(self):
        self.used_keywords: list[str] = []
        self.used_urls: list[str] = []
        self.summarizer = ResultSummarizerAgent()
    


    def check_for_google(self, text):
        words = text.split()
        if "GOOGLE" in words:
            return True
        else:
            return False
    


    def get_keyword_prompt(self, task: str):
        prompt = f"""I want to use the google search engine to search for: {task}, please return a list of keywords that I can use. """

        if self.used_keywords:
            message = f"(Don't use the following exact sets of keywords: {' or '.join(self.used_keywords)})"
            return prompt + message
        else:
            return prompt



    def get_analysis_prompt(self, summary: str, task: str):
        prompt = f"""My google search gave me the following result: '{summary}'.
            I was trying to solve the following problem: '{task}'.
            Did I get the information I wanted? If yes just return what you think I should store in my database. If not just return GOOGLE and I will try again. """
        return prompt
    


    def google(self, task: str, agent: AgentData, retry = 0) -> str:
        prompt = self.get_keyword_prompt(task)
        query = agent.open_ai.generate_text(prompt, 0.1)

        scraped_data = agent.browser.get_from_internet(query, self.used_urls)
        summary = self.summarizer.summarize(scraped_data, agent)

        agent.logger.log(f"Summary: {summary}")

        if self.check_for_google(summary) and retry < 3:
            return self.google(task, agent, retry + 1)
        else:
            self.used_urls = []
            self.used_keywords = []
            return summary
