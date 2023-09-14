## Art of Prompt Engineering

* Role Promopting - Enable the LLM to act as developer or writer, basically to inherit an identity.
* Few Shot Prompting - Guide the LLM with limited set of example responses that you expect. 
* Chain Prompting - Amplify reasoning with LLM output as input to next prompt.
* Prompt templates - Improve model context with dynamic prompting
* Create error free output formats by applying ouput parsing.
* Build knowledge graphs by discovering hidden relationhip.

A PromptTemplate is a pattern used to construct effective and consistent prompts for large language models. It is a guideline to ensure the input text or prompt is properly formatted.

## Prompts Examples:
### Good Prompts

```
Answer the question based on the context below. If the
question cannot be answered using the information provided, answer
with "I don't know".

Context: Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. 
...
Question: {query}
Answer: 
```

### Bad Prompts

- ```Tell me something about {topic}.```
This prompt is too-vague prompt that provides very little context for the model to generate a meaningful response.

- ```Tell me something about {genre1}, {genre2}, and {genre3} without giving any specific details.```
This prompt is unclear, as it asks for information about the genres but also states not to provide specific details. This makes it difficult for the LLM to generate a coherent and informative response. 
