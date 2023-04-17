from typing import Optional
from agents.IAgent import AgentData
from agents.ITask import Task


class TaskCreationAgent:
    def __init__(self):
        pass

    def create_tasks(self, last_task: Optional[Task] = None, agent: AgentData = None):
        
        if last_task is None:
            last_task = Task.empty()
        
        prompt = f'''
            You are a Task Creator Agent.

            Inputs:
            - Final Objective: {agent.objective}.
            - Previous task result: {last_task.result}
            - Previous task description: {last_task.description}

            Output: A JSON representing a new task based on the information in the input, following this schema:

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
                    "name": "scrape", // scrape a website
                    "input": a single url,
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
                    "result": None
                    }},
                    {{
                    "name": "scrape",
                    "input": "http://blabla.com",
                    "expected_output": "try to get info about the blabla website",
                    "result": None
                    }},
                    {{ ... }},
            ],
            "expected_output": "cheap accomodations including info from blabla site",
            "result": None
            }}
            '''

        response = agent.open_ai.generate_text(prompt)
        
        agent.logger.log(f"New Tasks: {response}")

        new_task = Task.from_json(response)

        agent.active_task = new_task