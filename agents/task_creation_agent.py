from agents.IAgent import AgentData
from agents.ITask import Task



class TaskCreationAgent:
    def __init__(self):
        self.used_keywords = list[str]



    def create_tasks(self, agent: AgentData = None):
        last_task = agent.active_task

        if last_task is None:
            last_task = Task.empty()
        else:
            agent.completed_tasks.append(last_task)
        
        #complete_string = " AND ".join(complete.description for complete in agent.completed_tasks)
       
        new_task_name = ""
        if last_task is not None and last_task.result is not None:
            new_task_name = last_task.result.new_task

        new_checklist = []
        if last_task is not None and last_task.result is not None:
            new_checklist = last_task.result.checklist
        
        prompt = f''' You are a Task Creator Agent. You want to {agent.objective}. 
                The name and checklist are given below:

                Current task name: {new_task_name}
                Checklist: {new_checklist}

                You need to write a JSON for the new task. JSON is a way of writing data in a structured format.
                This is the format of the JSON you need to write:

                Schema:
                {{
                "description": {new_task_name},
                "execution_agents": [
                {{
                "name": string,
                "input": string,
                "expected_output": string,
                }}
                ],
                "expected_output": string,
                }}

                Here are some notes and rules to help you write the JSON:
                    *"description" field should be the Current task name which is {new_task_name}.
                    *If there is no "description", use your own in the "description" field.
                    *The "execution_agents" field may include a maximum of four (4) agents. Use the execution_agents to try and solve the Checklist.
                    *The "name" field in the "execution_agents" array should be STRICTLY one of the following: "search_google" with keywords as input, "search_ddg" with keywords as input, or "scrape" with a website URL as input. You don't need to use them all, they can be used multiple times.
                    *The "scrape" agent can only be used if there is a website URL in the Checklist. Use that URL as the input for the “scrape” agent. If there is no website URL in the checklist, do not use the “scrape” agent at all.
                    *Do not use any other names for the "name" field in the "execution_agents" array other than "search_google", "search_ddg", or "scrape".
                    *The "input" field in the "execution_agents" should always be a string.
                    *The "expected_output" field should describe what is expected to be produced as output.

                Warning : If you break any of these rules, you will get a bad score and the task will be wrong. Especially DO NOT USE "scrape" if no URL in Checklist.

                Return only the JSON, no other comments please.
            '''

        #agent.logger.log(f"Creation Prompt: {prompt}")

        response = agent.open_ai.generate_text(prompt, 0.7)
        
        agent.logger.log(f"New Tasks: {new_task_name} - {response}")
        
        new_task = Task.from_json(response)
        
        # filter out execution_agents whose name is not within ["search_google", "foo"]
        new_task.execution_agents = [ea for ea in new_task.execution_agents if getattr(ea, 'name', '') in ["search_google", "search_ddg", "scrape"]]


        #agent.logger.log(f"New Task: {new_task.description}")

        agent.active_task = new_task