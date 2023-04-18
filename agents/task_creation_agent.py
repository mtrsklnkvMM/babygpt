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

        prompt = f''' You are a Task Creator Agent.
                Our global objective is to {agent.objective}.
                Current task name: {last_task.result}

                Checklist: []

                Output: A JSON representing the new task.

                Schema:
                {{
                "description": "",
                "execution_agents": [
                {{
                "name": string,
                "input": string,
                "expected_output": string,
                "result": string
                }}
                ],
                "expected_output": string,
                "result": string
                }}

                Notes:
                If there is no task name or checklist, it means it is the first task so use your own but always only return the JSON as output.

                The "execution_agents" field may include a maximum of four (4) agents. Use the execution_agents to try and solve the Checklist:
                The "name" field in the "execution_agents" array should be one of the following: "search_google" with keywords as input, "search_ddg" with keywords as input, or "scrape" with a website URL as input. You don't need to use them all, they can be used multiple times.
                If there is a URL we can use in the Checklist, use it for the “scrape” execution_agent. Otherwise, DO NOT USE the “scrape” execution_agent AT ALL.

                The "input" field in the "execution_agents" should always be a string.
                The "expected_output" field should describe what is expected to be produced as output.
                The "result" field should be left blank and will be filled in once the task is executed.
            '''

        agent.logger.log(f"Creation Prompt: {prompt}")

        response = agent.open_ai.generate_text(prompt, 0.7)
        
        agent.logger.log(f"New Tasks: {response}")
        
        new_task = Task.from_json(response)
        
        agent.active_task = new_task