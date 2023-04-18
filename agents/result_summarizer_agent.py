from agents.IAgent import AgentData
from agents.ITask import ExecutionAgent, Task
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
    
    def summarize(self, data: str, task: Task, agent: AgentData):
        result = self.summarize_text(data, 10)

        prompt = f"""Please provide a JSON output with the following format:
            - output_summary : Rewrite the following text: {result}. Include relevant information, interesting URL (https:... etc) and examples. Provide extensive information, and feel free to include as many particulars as possible. Please DO NOT create new content or provide your own analysis, just use the raw data. This is extremely important.
            - insights : Give a short list of insights (max 3) where the value is extremely important info from the summary.
            - grade : Judge the relevance of the final summary with regards to the expected outcome: "{task.expected_output}" (return "Grade: ?/10", 0 would be no relevant data), please be strict while assessing the quality of the base text in relation to the task.
            - new_tasks : Give a small list of follow up tasks based on the summary and the insights.

            Please provide as many particulars as possible and be as specific as you can. Include relevant information, interesting URL (https:... etc) and examples.

            Example JSON:
            {{
                "output_summary": "We discovered new types of medecines etc..",
                "insights": [
                    {{
                        "description": "Identified the main topic of the input text.",
                        "value": "Science"
                    }},
                    {{
                        "description": "Most important URL in the text",
                        "value": "https://blabla.com"
                    }},
                    {{...}}
                ],
                "grade": "5/10",
                "new_tasks": [
                    "Categorize Medecines",
                    "Investigate the URL https://blabla.com",
                    "summarize all previous tasks",
                     "etc..."
                ]
            }}
            """

        response = agent.open_ai.generate_text(prompt, 0.1)

        agent.logger.log(f"Task Summary: {response}")
        return response
    

    def reduceRawData(self, data: str, task: ExecutionAgent, agent: AgentData):
        result = self.summarize_text(data, 20)

        prompt = f"""Please rewrite the following text: {result}.
            Your summary should provide a clear overview of the main points discussed in the text, with a focus on information that is relevant to achieving the following outcome: {task.expected_output}.
            
            Please DO NOT create new content or provide your own analysis. Instead, focus on extracting relevant information and presenting it in a logical and easy-to-understand manner.
            
            Please include any URLs (https:... etc) or examples that help to illustrate the key points.
            Your summary should be comprehensive and detailed, and be at the very leats 2 paragraphs long.
            """

        response = agent.open_ai.generate_text(prompt, 0.1)

        agent.logger.log(f"Execution Agent Summary: {response}")
        return response