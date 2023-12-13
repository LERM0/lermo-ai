import os

from enum import Enum
from typing import List

# from pydantic import BaseModel
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.manager import CallbackManager

from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler
)

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

repo_paths = [
    ("/app/app/dataset/lermo_revealjs", [".md"], Language.MARKDOWN),
]

texts=[]

for repo_path, suffixes, language in repo_paths:
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=suffixes,
        parser=LanguageParser(language=language, parser_threshold=100)
    )
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_language(language=language, 
                                                                chunk_size=100, 
                                                                chunk_overlap=100)
    texts.extend(splitter.split_documents(documents))

print(f"{len(texts)} documents loaded.")

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
hf_embedding = HuggingFaceInstructEmbeddings()
db = FAISS.from_documents(texts, hf_embedding)

db.save_local("/app/app/dataset/faiss_lermo_ai_b")
print("Creating vectorstore.")