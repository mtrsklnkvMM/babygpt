import json
from agents.IAgent import AgentData
from agents.dispatcher_agent import DispatcherAgent
from agents.result_summarizer_agent import ResultSummarizerAgent



class ExecutionDispatcherAgent:
    def __init__(self):
        pass



    def executeAll(self, agent: AgentData):
        task = agent.active_task

        #agent.logger.log(f"""test: {task.description}""")

        if task is not None:
            for exec_agent in task.execution_agents:
                dispatcher = DispatcherAgent(exec_agent.name, agent)
                data = dispatcher.dispatch(exec_agent.input)
                raw_data = json.dumps(data)
                #agent.logger.log(f"""test2: {raw_data}""")
                full_result = ResultSummarizerAgent().reduceRawData(raw_data, exec_agent, agent)
                exec_agent.result = full_result
                
        full_result2 = ResultSummarizerAgent().summarize(task.execution_agents, task, agent)
        agent.active_task.result = full_result2