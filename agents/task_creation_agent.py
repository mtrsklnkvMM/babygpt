from agents.IAgent import AgentData
from agents.ITask import Task


class TaskCreationAgent:
    def __init__(self):
        pass

    def create_tasks(self, agent: AgentData = None):
        last_task = agent.active_task

        if last_task is None:
            last_task = Task.empty()
        else:
            agent.completed_tasks.append(last_task)
        
        complete_string = " AND ".join(complete.description for complete in agent.completed_tasks)

        prompt = f''' You are a Task Creator Agent. You create a task based on the following inputs:

            Inputs:
            - Final Objective: {agent.objective}.
            - Previous task result: {last_task.result}.

            Output: A JSON representing a new task that advances our objective, based on the insights and the new_tasks from the previous task:
            - description : short description of the task
            - execution_agents : please return a maximum of 3 execution_agents, you can select the same agent multiple times. Use information from the previous task.
            - expected_output : what to expect in the output based on the description
            
            This new task should NOT overlap with any previous tasks mentioned in : {complete_string}.
            
            Please follow this schema, this should be a valid JSON:

            {{
            "description": description of the new task,
            "execution_agents": [
                    {{
                    "name": "browse", // google search
                    "input": keywords for google search engine,
                    "expected_output": what is expected as output,
                    "result": keep empty
                    }},
                    {{
                    "name": "browse_ddg", // duck duck go search
                    "input": keywords for duck duck go search engine,
                    "expected_output": what is expected as output,
                    "result": keep empty
                    }},
                    {{
                    "name": "scrape", // scrape a website
                    "input": a single url coming from the previous results ONLY,
                    "expected_output": what is expected as output,
                    "result": keep empty
                    }}
            ],
            "expected_output": what to expect in the output based on the task description,
            "result": keep empty
            }}

            Here is an example that you should follow, please return a maximum of 3 execution_agents:

            {{
            "description": "find accomodation in London (...)",
            "execution_agents": [
                    {{
                    "name": "browse",
                    "input": "hotel London cheap",
                    "expected_output": "looking for a list of cheap hotels in London",
                    "result": ""
                    }},
                    {{
                    "name": "scrape",
                    "input": "http://blabla.com",
                    "expected_output": "try to get info about the blabla website",
                    "result": ""
                    }},
                    {{ ... }}
            ],
            "expected_output": "cheap accomodations including info from blabla site",
            "result": ""
            }}
            '''

        response = agent.open_ai.generate_text(prompt)
        
        agent.logger.log(f"New Tasks: {response}")
        
        new_task = Task.from_json(response)
        
        agent.active_task = new_task