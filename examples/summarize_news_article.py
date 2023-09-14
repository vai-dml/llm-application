# Develop an application that scraps online articles 
# and generate concice summary.

import requests
from newspaper import Article
from langchain.schema import (
    HumanMessage
)
from langchain.chat_models import ChatOpenAI

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
article_url = "https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"

def scrape_parse_article(article_url):

    session = requests.Session()
    try:
        response = session.get(article_url, headers=headers, timeout=10)
        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()
    
            return article.title, article.text
        else:
            print(f"Failed to fetch article at {article_url}")
    except Exception as e:
        print(f"Error occurred while fetching article at {article_url}: {e}")


def generate_summary():

    # we get the article data by calling the scraping function
    article_title, article_text = scrape_parse_article(article_url)
    print(f"Title: {article_title}")
    print(f"Text: {article_text}") 

    # Prompt construction - A well-crafted prompt ensures that the model understands the task, 
    # which in our case, involved summarizing an article into a bulleted list. 
    # By comprehending the nuances of prompt design, you can further tweak the model to generate outputs that suit unique needs.

    template = """"You are an advnaced assistant that summarizes online news articles into bullet points

    Here's the article you want to summarize.

    ==================
    Title: {article_title}

    {article_text}
    ==================

    Write a summary of the previous article.
    """

    prompt = template.format(article_title=article_title, article_text=article_text)
    messages = [HumanMessage(content=prompt)]

    # load the model
    chat = ChatOpenAI(model_name="gpt-4", temperature=0)
    
    # generate summary
    summary = chat(messages)
    print(summary.content)


generate_summary()