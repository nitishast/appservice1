import os
import config
import google.generativeai as genai
import streamlit as st

from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings # for vector embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS # for vector store db
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
import config
import time
groq_api_key = config.GROQ_API_KEY
pdf_directory = "./pdf_files"

# groqmodels = ["llama2-70b-4096","mixtral-8x7b-32768","gemma-7b-it"]


# Load the ChatGroq LLM and pass the API key
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="gemma-7b-it"  # You can change this to another model if needed
)


prompt = ChatPromptTemplate.from_template(
    "You are a helpful AI assistant. Answer questions based solely on the provided context. If the answer is not in the context, say 'The answer is not in the provided context.' Do not add any additional commentary or information beyond what is given.:\n\n{context}\n\nQuestion: {input}\nAnswer:"
)

def vector_embeddings(pdf_directory):
    if 'vector_store' not in st.session_state: # Persist data across Streamlit reruns
        start_time = time.time()
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Initialize embeddings model
        st.session_state.loader = PyPDFDirectoryLoader(pdf_directory)  # Create PDF directory loader
        st.session_state.documents = st.session_state.loader.load()  # Load documents from directory
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)  # Initialize text splitter
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.documents)  # Split documents into chunks
        st.session_state.vector_store = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings) 
        end_time = time.time() 
        st.session_state.vector_store_creation_time = end_time - start_time # Create FAISS vector store



def run():
    st.header("High-Performance Document Interaction: Leveraging GROQ API with Gemma 7B for Rapid Inference")

    prompt1 = st.text_input("Enter your question?")

    if st.button("Create Vector Store"):
        vector_embeddings(pdf_directory)
        st.write("Vector Store Created")
        st.write(f"Time Taken to create the vector store: {st.session_state.vector_store_creation_time: .2f} seconds")

    if prompt1:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vector_store.as_retriever()
        retreival_chain = create_retrieval_chain(retriever, document_chain)

        start = time.time()  # Change to time.time() for wall clock time
        response = retreival_chain.invoke({"input": prompt1})
        end = time.time()  # End timing
        response_time = end - start
        st.write(response["answer"])
        st.write(f"Time taken to get response from Groq API: {response_time:.2f} seconds")


        # with a streamlit expander
        with st.expander("Document Similiarity Search"):
            # find the relevant chunks
            for i,doc in enumerate(response["context"]):
                st.write(doc.page_content)
                st.write("--------------<><><><><><><><><>----------------")



