from agents.IAgent import AgentData



class TaskCreationAgent:
    def __init__(self):
        pass
    
    def extract_task_text(self, text):
        task_index = text.find("GOOGLE:")
        if task_index != -1:
            return text[task_index + len("GOOGLE:"):]
        else:
            return ""
    
    def get_problem_prompt(self, agent: AgentData):
        prompt = f"""You are a Planner Agent.
                You are trying to solve the following problem: "{agent.objective}".

                In order to solve this problem you might need multiple steps (over 10), this is just one of these step, keep that in mind."""
        return prompt

    def get_first_prompt(self):
        prompt = f"""
                Please imagine the very first step that is needed to solve this problem (be specific).
            """
        return prompt
    
    def get_step_prompt(self, tasks: str, database: str):
        prompt = f""" This is the list of steps we already took: {tasks}.
                We also stored this info in our database for context: "{database}".

                Please come up with the next step using information from this database dump in order to solve our problem (be specific).
            """
        return prompt
    
    def create_task(self, agent: AgentData):
        problem_prompt = self.get_problem_prompt(agent)
        main_prompt = self.get_first_prompt()

        if len(agent.completed_tasks) > 0:
            database_str = " ; ".join(d for d in agent.database)
            complete_string = " and ".join(complete for complete in agent.completed_tasks)
            main_prompt = self.get_step_prompt(complete_string, database_str)
        
        output_prompt = f"""
            Please go through your train of thoughts.

            We will be using google to solve this particular task.

            So end with the very specific query search/keywords (no placeholders! be very clear, return just 1 query) following this format (NOTE that google doesn't have access to the database ! only you):
            
            GOOGLE: ?
            
            example:
                GOOGLE: Cambridge Weather May 2023"""
        
        prompt = problem_prompt + main_prompt + output_prompt

        agent.logger.log(f"New Task Prompt: {prompt}")

        response = agent.open_ai.generate_text(prompt)

        agent.logger.log(f"New Task Response: {response}")

        new_task = self.extract_task_text(response)
        return new_task
