from typing import NamedTuple, Optional
from .ITask import Task
from agents.browser_agent import BrowserAgent
from agents.logger_agent import LoggerAgent
from completion.openai_provider import OpenAiProvider



class AgentData(object):
    def __init__(self, objective: str, active_task: Optional[Task], completed_tasks: list[Task],
                 open_ai: OpenAiProvider, browser: BrowserAgent, logger: LoggerAgent):
        self.objective = objective
        self.active_task = active_task
        self.completed_tasks = completed_tasks
        self.open_ai = open_ai
        self.browser = browser
        self.logger = logger