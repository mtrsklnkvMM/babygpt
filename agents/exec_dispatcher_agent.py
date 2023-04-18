import json
import re
from agents.IAgent import AgentData
from agents.ITask import ExecutionAgent, Task
from agents.dispatcher_agent import DispatcherAgent
from agents.result_summarizer_agent import ResultSummarizerAgent


class ExecutionDispatcherAgent:
    def __init__(self):
        pass


    def extract_grade(self, text):
        pattern = r"\bGrade:\s*(\d)/10\b"
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        else:
            return 10


    def executeAll(self, agent: AgentData):
        result = []
        task = agent.active_task

        agent.logger.log(f"""test: {task.description}""")

        if task is not None:
            for exec in task.execution_agents:
                exec_agent: ExecutionAgent = exec
                dispatcher = DispatcherAgent(exec_agent.name, agent)
                r = dispatcher.dispatch(exec_agent.input)
                rr = json.dumps(r)
                full_result = ResultSummarizerAgent().summarize2(rr, exec_agent, agent)
                exec_agent.result = full_result
                result.append(r)
        
        result_dump = [json.dumps(execution_agent.result) for execution_agent in task.execution_agents]
        full_result2 = ResultSummarizerAgent().summarize(" AND ".join(result_dump), task, agent)
        agent.active_task.result = full_result2