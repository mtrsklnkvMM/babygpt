from agents.IAgent import AgentData
from agents.exec_dispatcher_agent import ExecutionDispatcherAgent
from agents.task_creation_agent import TaskCreationAgent


class TaskProcessor:
    def __init__(self):
        self.task_creation_agent = TaskCreationAgent()
        self.execution_agent = ExecutionDispatcherAgent()

    def process_task(self, agent: AgentData):
        task_with_results = self.execution_agent.dispatch(agent)
        agent.completed_tasks.append(task_with_results)
        self.task_creation_agent.create_tasks(task_with_results, agent)