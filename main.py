#!/usr/bin/env python3
import os
import time
from collections import deque
from typing import Optional
from dotenv import load_dotenv
from agents.IAgent import AgentData
from agents.ITask import Task
from agents.browser_agent import BrowserAgent
from agents.logger_agent import LoggerAgent
from agents.task_prioritiser_agent import ObjectiveCompletionAgent
from completion.openai_provider import OpenAiProvider
from task.task_processor import TaskProcessor

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"
BROWSER_API_KEY = os.getenv("BROWSER_API_KEY", "")
BROWSER_API_ENGINE = os.getenv("BROWSER_API_ENGINE", "")
assert BROWSER_API_KEY, "BROWSER_API_KEY environment variable is missing from .env"

browser_agent = BrowserAgent(BROWSER_API_KEY, BROWSER_API_ENGINE)
openai_provider = OpenAiProvider(OPENAI_API_KEY)
logger = LoggerAgent()
task_processor = TaskProcessor()
current_task: Optional[Task] = None
completed_tasks = deque([])

OBJECTIVE = os.getenv("OBJECTIVE", "")

agent_data = AgentData(objective=OBJECTIVE,
                       active_task=current_task,
                       completed_tasks=completed_tasks,
                       open_ai=openai_provider,
                       browser=browser_agent,
                       logger=logger)

logger.log(f"Starting solving: {agent_data.objective}")

for day in range(1, 6):
    logger.log(f"Day {day}: Starting Task > ")
    
    task_processor.process_task(agent_data)
    
    time.sleep(1)

ObjectiveCompletionAgent().conclude(agent_data)
logger.close()