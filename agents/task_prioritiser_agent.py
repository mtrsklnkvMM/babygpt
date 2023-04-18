from agents.IAgent import AgentData


class ObjectiveCompletionAgent:
    def __init__(self):
        pass
        
    def conclude(self,  agent: AgentData):
        description_string = " AND ".join(task.result for task in agent.completed_tasks)

        if len(description_string) > 6000:
                description_string = description_string[:6000] + '...'

        prompt = f"""You are task to address {agent.objective}:

        Input:
        - Objective: {agent.objective}.
        - Completed tasks: {description_string}.

        Ouput:
        - Write a comprehensive answer to our objective using only the result from the completed tasks.
        DO NOT make up things, just use the data available, this is extremely important. Please be very specific and provide lots of details.
        -Assess your work at the very end give yourself a grade
        -Give a few new objective ideas."""
        
        agent.logger.log(f"""Conclusion Prompt: {prompt}""")
        response = agent.open_ai.generate_text(prompt)
        agent.logger.log(f"""Conclusion: {response}""")