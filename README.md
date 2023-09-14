# llm-building-using-activeloop
HandsOn LLM applications using LangChain and Deep Lake. Langchain gives developers a set of tools and components to build LLM powered applications.


## Data Points

* The maximum number of tokens the model can process, is determined by the specific implementation of the LLM. Each model has token limit it can take in. Split the text into smaller chunks to handle large inputs.
* Few shot learning is the ability that allows LLMs to learn and genralize from limited examples. Examples can be both hard coded or dynamically selected and can be feeded to the LLM.
* occurrence of hallucinations - models can produce text that appears plausible on the surface but is actually factually incorrect or unrelated to the given input.
* LLMs may exhibit biases originating from their training data, resulting in outputs that can generate undesired outcomes.
* LLM examples include Text Summarization, Text Translation, and Question Answering
* Well-known models like GPT family, LLaMA employ subword level tokenization method. One of the variant used is Byte Pair Encoding (BPE)

## The Chains

In LangChain, a chain is an end-to-end wrapper around multiple individual components, providing a way to accomplish a common use case by combining these components in a specific sequence. The most commonly used type of chain is the LLMChain, which consists of a PromptTemplate, a model (either an LLM or a ChatModel), and an optional output parser.

The LLMChain works as follows:

Takes (multiple) input variables.
Uses the PromptTemplate to format the input variables into a prompt.
Passes the formatted prompt to the model (LLM or ChatModel).
If an output parser is provided, it uses the OutputParser to parse the output of the LLM into a final format.

## The Memory
In LangChain, Memory refers to the mechanism that stores and manages the conversation history between a user and the AI. It helps maintain context and coherency throughout the interaction, enabling the AI to generate more relevant and accurate responses. Memory, such as ConversationBufferMemory, acts as a wrapper around ChatMessageHistory, extracting the messages and providing them to the chain for better context-aware generation.

## Deep Lake Vector Store

Deep Lake provides storage for embeddings and their corresponding metadata in the context of LLM apps. It enables hybrid searches on these embeddings and their attributes for efficient data retrieval. It also integrates with LangChain, facilitating the development and deployment of applications.

Deep Lake provides several advantages over the typical vector store:

It’s multimodal, which means that it can be used to store items of diverse modalities, such as texts, images, audio, and video, along with their vector representations. 
It’s serverless, which means that we can create and manage cloud datasets without creating and managing a database instance. This aspect gives a great speedup to new projects.
Last, it’s possible to easily create a data loader out of the data loaded into a Deep Lake dataset. It is convenient for fine-tuning machine learning models using common frameworks like PyTorch and TensorFlow.

## Deep Lake Vector Store

In LangChain, agents are high-level components that use language models (LLMs) to determine which actions to take and in what order. An action can either be using a tool and observing its output or returning it to the user. Tools are functions that perform specific duties, such as Google Search, database lookups, or Python REPL.

Agents involve an LLM making decisions about which Actions to take, taking that Action, seeing an Observation, and repeating that until done.

Several types of agents are available in LangChain:

The zero-shot-react-description agent uses the ReAct framework to decide which tool to employ based purely on the tool's description. It necessitates a description of each tool.
The react-docstore agent engages with a docstore through the ReAct framework. It needs two tools: a Search tool and a Lookup tool. The Search tool finds a document, and the Lookup tool searches for a term in the most recently discovered document.
The self-ask-with-search agent employs a single tool named Intermediate Answer, which is capable of looking up factual responses to queries. It is identical to the original self-ask with the search paper, where a Google search API was provided as the tool.
The conversational-react-description agent is designed for conversational situations. It uses the ReAct framework to select a tool and uses memory to remember past conversation interactions.






 