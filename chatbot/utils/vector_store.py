# from langchain.vectorstores import FAISS
# from langchain.embeddings.openai import OpenAIEmbeddings

# def create_vector_store(text):

#     embeddings = OpenAIEmbeddings()

#     db = FAISS.from_texts([text],embeddings)

#     db.save_local("faiss_db")

#     return db


import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def create_vector_store(text):

    embeddings = OpenAIEmbeddings()

    vector_db = FAISS.from_texts(
        [text],
        embeddings
    )

    vector_db.save_local("faiss_db")

    return vector_db