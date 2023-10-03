# Develop an application that scraps online articles 
# and generate concice summary.

import requests
from newspaper import Article

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate 
from langchain.output_parsers import PydanticOutputParser
from pydantic import validator
from pydantic import BaseModel, Field
from typing import List


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
article_url = "https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"


# create output parser class
class ArticleSummary(BaseModel):
    title: str = Field(description="Title of the article")
    summary: List[str] = Field(description="Bulleted list summary of the article")

    # validating whether the generated summary has at least three lines
    @validator('summary', allow_reuse=True)
    def has_three_or_more_lines(cls, list_of_lines):
        if len(list_of_lines) < 3:
            raise ValueError("Generated summary has less than three bullet points!")
        return list_of_lines


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

    # Prompt construction - A well-crafted prompt ensures that the model understands the task, 
    # which in our case, involved summarizing an article into a bulleted list. 
    # By comprehending the nuances of prompt design, you can further tweak the model to generate outputs that suit unique needs.

    template = """"You are an advnaced assistant that summarizes online news articles into bullet points

    Here's the article you want to summarize.

    ==================
    Title: {article_title}

    {article_text}
    ==================

    {format_instructions}
    """
    
    # set up output parser
    parser = PydanticOutputParser(pydantic_object=ArticleSummary)

    prompt = PromptTemplate(
        template==template,
        input_variables=["article_title", "article_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Format the prompt using the article title and text obtained from scraping
    formatted_prompt = prompt.format_prompt(article_title=article_title, article_text=article_text)

    # load the model
    model = OpenAI(model_name="text-davinci-003", temperature=0.0)

    # Use the model to generate a summary
    output = model(formatted_prompt.to_string())        
    
    # Parse the output into the Pydantic model
    parsed_output = parser.parse(output)
    print(parsed_output)


generate_summary()