import openai
import ray
import io

from tqdm import tqdm

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake
from typing import List, Any, Optional, Dict
from ray.data.datasource import FileExtensionFilter


# Initialize the OpenAIEmbeddings instance
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Read the PDF documents in raw format
data_source = ray.data.read_binary_files("examples/data/arxiv_pdfs/", partition_filter=FileExtensionFilter("pdf"))

# Convert raw PDF bytes and parse them as text
def convert_to_text(pdf_bytes: bytes):
    pass
    
    

def split_text_to_chunks(text: str):
    """
    Splitting text into chunks

    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )

    split_text: List[str] = text_splitter.split_text(text)
    split_text = [text.replace("\n", " ") for text in split_text]
    return split_text

