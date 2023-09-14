from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


# Before executing the following code, make sure to have
# your OpenAI key saved in the “OPENAI_API_KEY” environment variable.
llm = OpenAI(model="text-davinci-003", temperature = 0.9)

prompt = PromptTemplate(
    input_variable = ["product"],
    template = "What is a good name for a company that makes {product}?"
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("eco-friendly water bottles"))

