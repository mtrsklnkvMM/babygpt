from agents.IAgent import AgentData
from web_browser.web_browser_agent import ExecutionDispatcherAgent, WebBrowserAgent
from agents.task_creation_agent import TaskCreationAgent


class TaskProcessor:
    def __init__(self):
        self.task_creation_agent = TaskCreationAgent()
        self.web_agent = WebBrowserAgent()

    def process_task(self, agent: AgentData):
        new_task = self.task_creation_agent.create_task(agent)
        
        data_to_save = self.web_agent.google(new_task, agent)
        agent.logger.log(f"Save: {data_to_save}")
        
        agent.completed_tasks.append(new_task)
        agent.database = agent.database + " ; " + data_to_save