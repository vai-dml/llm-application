from langchain import FewShotPromptTemplate, PromptTemplate, LLMChain
from langchain.llms import Cohere

# your key goes her
COHERE_API_KEY = ""

# Inititalize llm
llm = Cohere(cohere_api_key=COHERE_API_KEY)


# By providing relevant examples, the LLM can better understand 
# the style and tone of the responses it should produce. 
examples = [
    {
        "query": "What's is Mixed Martial Arts(MMA)?",
        "answer": "MMA is a full-contact combat sport. It offers various disciplines like Muay Thai, Boxing and Brazilian jiu-jitsu."
    }, {
        "query": "How do I choose a discipline?",
        "answer": "Try choosing a discipline by enrolling to trail classes and accessing factors like physical endurance and coaching standard."
    }

]

example_template = """
User: {query}
AI: {answer}
"""

example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

# This context helps guide the AI's responses and ensures they align with the intended purpose.
prefix = """The following are excerpts from conversations with an AI
Mixed Martial Arts coach. The assistant provides insightful and practical advice to the users' questions. Here are some
examples: 
"""

# This helps maintain a clear and consistent format for the generated responses.
suffix = """
==================
User: {query}
AI: 
==================

Write a answer to the query in number points.
"""

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)

# Create the LLMChain for the few-shot prompt template
chain = LLMChain(llm=llm, prompt=few_shot_prompt_template)

# Define the user query
user_query = "What are some tips for improving strength and agilty?"

# Run the LLMChain for the user query
response = chain.run({"query": user_query})

# The output generated is not consistent in terms of format. Usefull to add some validation of the output schema/format.
print("User Query:", user_query)
print("AI Response:", response)
