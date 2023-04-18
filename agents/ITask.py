import json
from typing import NamedTuple, Optional


class TaskResult(NamedTuple):
    output_summary: str
    grade: str
    new_task: str
    checklist: list[str]



class ExecutionAgent:
    def __init__(self, name, input, expected_output, result):
        self.name = name
        self.input = input
        self.expected_output = expected_output
        self.result = result

    @classmethod
    def from_dict(cls, agent_dict):
        try:
            name = agent_dict['name']
            input_val = agent_dict['input']
            expected_output = agent_dict['expected_output']
            result = agent_dict['result']
        except (KeyError, TypeError):
            # Return an empty ExecutionAgent instance if there is an error getting any required data from the dict
            return cls("", "", "")
        
        return cls(name=name,
                   input=input_val,
                   expected_output=expected_output,
                   result=result)
    


class Task:
    def __init__(self, description, execution_agents: list[ExecutionAgent], expected_output, result: Optional[TaskResult] = None):
        self.description = description
        self.execution_agents = execution_agents
        self.expected_output = expected_output
        self.result = result

    @classmethod
    def empty(cls):
        return cls("", [], "")
    

    @classmethod
    def from_json(cls, json_string):
        try:
            print(json_string)
            json_dict = json.loads(json_string)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"An error occurred while parsing JSON: {e}")
            # Return an empty task if there is an error parsing the JSON string
            return cls("", [], "")
        
        execution_agents = []
        for agent_dict in json_dict.get('execution_agents', []):
            try:
                agent = ExecutionAgent.from_dict(agent_dict)
                execution_agents.append(agent)
            except TypeError:
                print("error")
                # If there is an error creating an ExecutionAgent instance, skip that agent
                pass
        
        # Return an empty task if there is an error getting any required data from the JSON
        try:
            description = json_dict['description']
            expected_output = json_dict['expected_output']
            result = json_dict.get('result', None)
        except (KeyError, TypeError):
            print("error1")
            return cls("", [], "")
        
        return cls(description=description,
                   execution_agents=execution_agents,
                   expected_output=expected_output,
                   result=result)