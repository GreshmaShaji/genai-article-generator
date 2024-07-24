import requests
from transformers import pipeline
from langchain_core.runnables import Runnable, RunnableSequence, RunnableLambda
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Function to fetch a summary from Wikipedia
def fetch_wikipedia_summary(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['extract']
    else:
        return "No information available."

# Function to generate text using GPT-2
def generate_text(input_text):
    generator = pipeline('text-generation', model='gpt2')
    result = generator(input_text, max_length=500, num_return_sequences=1)
    generated_text = result[0]['generated_text']
    
    # Split the generated text into three paragraphs
    paragraphs = generated_text.split('\n\n')
    if len(paragraphs) < 3:
        # If less than 3 paragraphs, split by sentences and group into 3 parts
        sentences = generated_text.split('. ')
        third = len(sentences) // 3
        paragraphs = ['. '.join(sentences[:third]), '. '.join(sentences[third:2*third]), '. '.join(sentences[2*third:])]
    
    return '\n\n'.join(paragraphs[:3])

# Function to generate a headline using a summarization model
def generate_headline(input_text):
    summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')
    result = summarizer(f"Create a headline for this article summary: {input_text}", max_length=10, min_length=5, do_sample=False, truncation=True)
    return result[0]['summary_text']

# Custom Runnable components
class WikipediaSummaryStep(Runnable):
    def invoke(self, inputs, config=None):
        query = inputs['query']
        retrieved_info = fetch_wikipedia_summary(query)
        inputs['retrieved_info'] = retrieved_info
        return inputs

class ArticleGenerationStep(Runnable):
    def invoke(self, inputs, config=None):
        retrieved_info = inputs['retrieved_info']
        input_text = f"{retrieved_info}\n\nIn conclusion,"
        article = generate_text(input_text)
        inputs['article'] = article
        return inputs

class HeadlineGenerationStep(Runnable):
    def invoke(self, inputs, config=None):
        article = inputs['article']
        headline = generate_headline(article)
        return {'headline': headline, 'article': article}

# Create instances of the custom steps
wikipedia_summary_step = WikipediaSummaryStep()
article_generation_step = ArticleGenerationStep()
headline_generation_step = HeadlineGenerationStep()

# Combine the steps using the pipe operator
sequence = wikipedia_summary_step | article_generation_step | headline_generation_step

# Function to create the newspaper article using the sequence
def create_newspaper_article(query):
    inputs = {
        'query': query
    }
    results = sequence.invoke(inputs)
    return results

query = input("Enter a topic here to generate the article : ")
result = create_newspaper_article(query)
print("Headline:", result['headline'])
print("Article:", result['article'])
