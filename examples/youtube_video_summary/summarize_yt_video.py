"""
LLM Flow 1

Load Youtube Video URL -> Download Video -> Transcribe Video (Open AI Whisper)
-> Create summaraization chain -> Generate Summary 

LLM Flow 2

Load Youtube Video URL -> Download Video -> Transcribe Video 
-> Create summaraization chain -> Split to chunks -> Convert to embedding 
-> Store in Vector Db -> Prepare Prompts -> Retrieve from Vector DB -> Generate Summary (Retrieval QA) 

"""

import os
import yt_dlp
import whisper
import ssl
import textwrap
from langchain.llms import Cohere
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import DeepLake
from langchain.embeddings import CohereEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

ssl._create_default_https_context = ssl._create_unverified_context
os.environ['COHERE_API_KEY'] = ""
os.environ['OPEN_API_KEY'] = ""
os.environ['ACTIVELOOP_TOKEN'] = ""

# adding multiple URLs
def download_yt_video(urls, job_id):

    # This will hold the titles and authors of each downloaded video
    video_info = []

    for i, url in enumerate(urls):
         # Set the options for the download
        file_temp = f'./{job_id}_{i}.mp4'
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': file_temp,
            'quiet': True,
        }
    
        # Download the video file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url=url, download=True)
            title = result.get('title', "")
            author = result.get('uploader', "")

        # Add the title and author to our list
        video_info.append((file_temp, title, author))
    
    return video_info


def transcribe_video(videos_details):

    model = whisper.load_model('base')
    # iterate through each video and transcribe
    results = []
    for v in videos_details:
        print('v',v)
        result = model.transcribe(v)
        results.append(result['text'])
    
    with open ('transcribe_output.txt', 'w') as file:  
        file.write(results['text'])


def chunk_and_split():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )
    with open('transcribe_output.txt') as f:
        text = f.read()

    texts = text_splitter.split_text(text)
    # The [:4] slice notation indicates that only the first four chunks will be used to create the Document objects. 
    docs = [Document(page_content=t) for t in texts[:4]]
    return docs



def get_retriever():
    # create Deep Lake dataset
    # TODO: use your organization id here. (by default, org id is your username)
    my_activeloop_org_id = "vai"
    my_activeloop_dataset_name = "youtube_summarizer"
    dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"

    embeddings = CohereEmbeddings(cohere_api_key=os.getenv('COHERE_API_KEY'))
    db = DeepLake(dataset_path=dataset_path,embedding_function=embeddings)
    docs = chunk_and_split()
    db.add_documents(docs)

    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['k'] = 4

    return retriever


def summarize():

    # initialise llm
    llm = Cohere(cohere_api_key=os.getenv('COHERE_API_KEY'))

    # create prompt
    prompt_template = """Use the following pieces of transcripts from a video to answer the question in bullet points and summarized. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Summarized answer in bullter points:"""
    
    PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
    )

    # create a end to end chain pipeline
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA(
        llm= llm,
        # The 'refine' summarization chain is a method for generating more accurate and context-aware summaries.
        chain_type="refine",
        retriever= get_retriever(),
        chain_type_kwargs=chain_type_kwargs
    )

    # Generate summary
    output_summary = qa.run("Summarize the mentions of google according to their AI program")
    print(output_summary)


urls=["https://www.youtube.com/watch?v=mBjPyte2ZZo&t=78s",
    "https://www.youtube.com/watch?v=cjs7QKJNVYM",]
# Use the below methods for initial loading and transcribing the video.
# videos_details = download_yt_video(urls, 1)

video_details=["1_0.mp4","1_1.mp4"]
transcribe_video(video_details)

# make sure the above methods are commented before calling summarize method.
#summarize()

