from typing import NamedTuple
from vector.weaviate import Weaviate
from web_browser.browser_agent import BrowserAgent
from agents.logger_agent import LoggerAgent
from completion.openai_provider import OpenAiProvider


class AgentData(NamedTuple):
    objective: str
    completed_tasks: list[str]
    database: list[str]
    vectordb: Weaviate
    open_ai: OpenAiProvider
    browser: BrowserAgent
    logger: LoggerAgent