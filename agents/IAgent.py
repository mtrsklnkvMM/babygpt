from typing import NamedTuple, Optional
from .ITask import Task
from agents.browser_agent import BrowserAgent
from agents.logger_agent import LoggerAgent
from completion.openai_provider import OpenAiProvider


class AgentData(NamedTuple):
    objective: str
    active_task: Optional[Task]
    completed_tasks: list[Task]
    open_ai: OpenAiProvider
    browser: BrowserAgent
    logger: LoggerAgent
    