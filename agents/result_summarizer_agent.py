import json
import re
from agents.IAgent import AgentData
from agents.ITask import ExecutionAgent, Task, TaskResult
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


class ResultSummarizerAgent:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        pass



    def summarize_text(self, text, num_sentences=10, chunk_size=1000000):
        summaries = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            doc = self.nlp(chunk)
            stopwords = list(STOP_WORDS)
            word_frequencies = {}
            for word in doc:
                if word.text.lower() not in stopwords:
                    if word.text.lower() not in punctuation:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1

            max_frequency = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/max_frequency)

            sentence_tokens = [sent for sent in doc.sents]
            sentence_scores = {}
            for sent in sentence_tokens:
                for word in sent:
                    if word.text.lower() in word_frequencies.keys():
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

            summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
            final_sentences = [w.text for w in summary_sentences]
            summary = ' '.join(final_sentences)
            
            # Limit summary to a maximum of 4000 characters
            if len(summary) > 6000:
                summary = summary[:6000] + '...'
                
            summaries.append(summary)
        
        return ' '.join(summaries)
    

    def extract_grade(self, text):
        pattern = r"\bGrade:\s*(\d)/10\b"
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        else:
            return 10
        

    
    def summarize(self, exec_agents: list[ExecutionAgent], task: Task, agent: AgentData):
        results = []
        for exec_agent in exec_agents:
            grade = self.extract_grade(exec_agent.result)
            if grade > 4:
                results.append(exec_agent.result)
        
        data = json.dumps(results)
        #agent.logger.log(f"Task data: {data}")
        result = self.summarize_text(data, 10)

        prompt = f"""Please provide a JSON output with the following format:

            - output_summary : Rewrite the following text: "{result}". Include all relevant information, interesting URL (https:... etc) and examples. Provide extensive information, and feel free to include as many particulars as possible. Please DO NOT create new content or provide your own analysis, just use the raw data. This is extremely important.
                        
            - grade : Judge the relevance of the final summary with regards to the expected outcome: "{task.expected_output}" (return "Grade: ?/10", 0 would be no relevant data), please be strict while assessing the quality of the base text in relation to the task.
                        
            - new_task : Based on the output summary and our global objective "{agent.objective}" , come up with a relevant follow up task description.

            - checklist : List of the things to do to complete the new_task. Be specific and concise. Include URL/names/keywords to search etc.

            Example JSON:
            {{
                "output_summary": "We discovered new types of medecines...",
                "grade": "5/10",
                "new_task": "Categorize Medecines",
                "checklist": [
					"check the following site https://blabla.com",
					"Search for this medecine in particular",
					"etc..."
				]
            }}
            """

        response = agent.open_ai.generate_text(prompt, 0.5)

        # Parse the JSON string as a dictionary
        input_dict = json.loads(response)

        # Create a TaskResult instance using the NamedTuple constructor
        task_result = TaskResult(**input_dict)

        agent.logger.log(f"Task Summary: {task.description} - {response}")
        return task_result
    

    def reduceRawData(self, data: str, task: ExecutionAgent, agent: AgentData):
        result = self.summarize_text(data, 10)
        #agent.logger.log(f"reduceRawData: {task.name}")
        #agent.logger.log(f"Original Raw Data: {result}")

        prompt = f"""Please provide a comprehensive and detailed summary of the following text: {result}.
            
                    Please provide names, places or URLs (https:... etc) that help to illustrate these points.

                    Avoid adding your own analysis or opinions; instead, focus on presenting the information in an objective manner.

                    Finally, please include a list of potential follow-up tasks based on the insights and observations presented in the summary. These tasks should be actionable and relevant to the objective at hand ({task.expected_output}), and could include tasks related to research, data analysis, or further investigation.
                    
                    Note: Judge the relevance of the final summary with regards to the expected outcome: "{task.expected_output}" (return "Grade: ?/10", 0 would be no relevant data), please be strict while assessing the quality of the base text in relation to the task.
                 """

        response = agent.open_ai.generate_text(prompt, 0.1)

        agent.logger.log(f"Execution Agent Summary: {task.name} - {response}")
        return response