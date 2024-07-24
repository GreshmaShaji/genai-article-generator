# genai-article-generator

## Overview
This project is designed to demonstrate the use of Retrieval-Augmented Generation (RAG) and LangChain technology to build a context-aware newspaper article generator. The tool retrieves relevant information from Wikipedia based on a user query, generates a brief article in three paragraphs, and creates a catchy headline for the article.


## Features
- Retrieval-Augmented Generation (RAG): Retrieves contextually relevant information from Wikipedia to enhance the quality and relevance of generated articles.
- LangChain Integration: Utilizes LangChain's Runnable components to create a modular and composable sequence of operations for article generation.
- Text Generation and Summarization: Employs GPT-2 for text generation and a summarization model for headline creation.

## Installation
1. Clone the Repository
```
git clone https://github.com/greshmashaji/genai-article-generator.git
cd genai-article-generator
```
2. Create a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install Dependencies

```
pip install -r requirements.txt
```

## Usage
Run the Script:
```
python originalArticle.py
```

## Code Explanation

### fetch_wikipedia_summary(query)
Fetches a summary from Wikipedia based on the provided query.

### generate_text(input_text)
Generates an article using GPT-2 and ensures it is split into three paragraphs.

### generate_headline(input_text)
Generates a catchy headline using a summarization model.

### WikipediaSummaryStep(Runnable)
Retrieves information from Wikipedia and adds it to the inputs.

### ArticleGenerationStep(Runnable)
Generates an article using the retrieved information and ensures it is three paragraphs.

### HeadlineGenerationStep(Runnable)
Generates a headline for the article using the summarization model.

### create_newspaper_article(query)
Combines the custom steps using LangChain's RunnableSequence to create the final article and headline.


