from agents.IAgent import AgentData



class TaskCreationAgent:
    def __init__(self):
        pass
    
    def extract_task_text(self, text):
        task_index = text.find("TASK:")
        if task_index != -1:
            return text[task_index + len("TASK:"):]
        else:
            return ""
    
    def get_problem_prompt(self, agent: AgentData):
        prompt = f"""
                We are trying to solve the following problem: {agent.objective}.
                In order to solve this objective we might need multiple steps (over 10), this is just one of these step."""
        return prompt

    def get_first_prompt(self):
        prompt = f"""
                Please come up with the very first task that is necessary to complete this objective.
            """
        return prompt
    
    def get_step_prompt(self, tasks: str, database: str):
        prompt = f""" This is the list of task we completed: {tasks}.
                We already have all this information saved in our database: {database}.
                Please come up with the next task that is necessary to complete this objective.
            """
        return prompt
    
    def create_task(self, agent: AgentData):
        problem_prompt = self.get_problem_prompt(agent)
        main_prompt = self.get_first_prompt()

        if len(agent.completed_tasks) > 0:
            complete_string = " and ".join(complete for complete in agent.completed_tasks)
            main_prompt = self.get_step_prompt(complete_string, agent.database)
        
        output_prompt = f"""
            We will be using google to retrieve information.

            Please explain your train of thoughts and then end with:
            TASK: [task 1 or 2 sentences max]"""
        
        prompt = problem_prompt + main_prompt + output_prompt

        response = agent.open_ai.generate_text(prompt)

        agent.logger.log(f"New Task Response: {response}")

        new_task = self.extract_task_text(response)
        return new_task
