"""The code that was used to generate the document dataset.

1. Make a search query to arxiv for the 2000 documents most relevant to topic
2. For each result, download the PDF locally to a directory, with some error handling.
3. Upload the PDF to local directory.
"""

import time
from urllib.error import HTTPError
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import arxiv
from tqdm import tqdm

search_results = arxiv.Search(
    query="Data Architecture",
    max_results=500,
)

for result in tqdm(search_results.results()):
    while True:
        try:
            result.download_pdf(dirpath="./arxiv_pdfs")
            break
        except FileNotFoundError:
            print("file not found")
            break
        except HTTPError:
            print("forbidden")
            break
        except ConnectionResetError as e:
            print("connection reset by peer")

            # wait for some time before retrying the connection
            time.sleep(5)