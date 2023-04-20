import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import defaultdict

class ResultSummarizerAgent:
    def __init__(self):
        self.reputable_sources = [
            # News sources
            "reuters.com",
            "apnews.com",
            "nytimes.com",
            "washingtonpost.com",
            "bbc.com/news",
            "cnn.com",
            "theguardian.com",
            "aljazeera.com",
            "economist.com",
            "bloomberg.com",
            
            # Academic sources
            "pubmed.ncbi.nlm.nih.gov",
            "arxiv.org",
            "scholar.google.com",
            "jstor.org",
            "sciencedirect.com",
            "ieeexplore.ieee.org",
            "dl.acm.org",
            "journals.plos.org/plosone",
            "nature.com",
            "sciencemag.org",
            
            # Travel sources
            "tripadvisor.com",
            "lonelyplanet.com",
            "fodors.com",
            "roughguides.com",
            "frommers.com",
            "nationalgeographic.com/traveler",
            "cntraveler.com",
            "travelandleisure.com",
            "ricksteves.com",
            "afar.com"
        ]
        self.nlp = spacy.load('en_core_web_sm')
        

    def get_domain(link):
        # Extract domain name from link using regex
        match = re.search(r'(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', link)
        if match:
            return match.group(3)
        else:
            return None


    def prioritize_links(self, response, query, used_urls: list[str]):
        keywords = self.nlp(query).text.split()
        priorities = []

        for item in response['items']:
            link = item['link']
            domain = self.get_domain(link)
            snippet = item.get('snippet')
            title = item.get('title')
            score = 0
        
        if domain in self.reputable_sources:
            score += 2
        
        for keyword in keywords:
            if snippet and keyword in snippet.lower() or title and keyword in title.lower():
                score += 1
        if link in used_urls:
            score -= 10
        
        priorities.append((link, score))
    
        priorities.sort(key=lambda x: x[1], reverse=True)
    
        return [p[0] for p in priorities]
    

    def trim_sorted_sentences(self, sorted_sentences, max_length = 6000):
        # Initialize a list to store the extracted sentences
        extracted_sentences = []

        # Iterate over the sorted sentences and add them to the list until the total length exceeds the limit
        total_length = 0
        for sent, score in sorted_sentences:
            sent_text = sent.text.strip()
            sent_length = len(sent_text)
            
            # Check if adding the current sentence would exceed the maximum length
            if total_length + sent_length > max_length:
                break
            
            # Add the current sentence to the list and update the total length
            extracted_sentences.append(sent_text)
            total_length += sent_length

        # If the extracted sentences are still too long, trim the last sentence until the total length is within the limit
        while total_length > max_length and extracted_sentences:
            last_sentence = extracted_sentences.pop()
            total_length -= len(last_sentence)
            
        # Return the extracted sentences
        return extracted_sentences
    

    def summarize_text(self, text, chunk_size=1000000):
        summaries = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            doc = self.nlp(chunk)
            num_tokens = len(doc)
            print(num_tokens)

            # Build a list of sentences and their corresponding TextRank scores
            sentence_scores = defaultdict(float)
            for sent in doc.sents:
                for word in sent:
                    if word.text.lower() not in STOP_WORDS:
                        sentence_scores[sent] += word.rank

            # Sort the sentences by their TextRank scores in descending order
            sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

            # Extract the top N sentences based on their TextRank scores
            top_sentences = self.trim_sorted_sentences(sorted_sentences)

            # Join the top sentences together into a single summary string
            summary = '\n'.join(top_sentences)

            # Limit summary to a maximum of 4000 characters
            if len(summary) > 6000:
                summary = summary[:6000] + '...'
            
            summaries.append(summary)
        
        return ' '.join(summaries)
    
    
    
    def summarize(self, text: str, agent):
        result = self.summarize_text(text)

        prompt = f"""Please rewrite this text to make it cleaner: "{result}"."""

        response = agent.open_ai.generate_text(prompt, 0.1)

        agent.logger.log(f"Task Summary: {response}")
        return response