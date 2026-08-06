import os
import re
import shutil
import warnings
import logging
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)
import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_cohere import CohereEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_cohere import CohereRerank
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Importaciones necesarias para la arquitectura LCEL
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
#from langchain.output_parsers import JsonOutputParser
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import time
from langchain_core.runnables import RunnableLambda
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Annoy
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from ddgs import DDGS
from langchain.messages import HumanMessage, ToolMessage

import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

load_dotenv(find_dotenv())




@tool
def google_search(query:str)->str:
    """Busca en internet usando DuckDuckGo Search y devuelve los resultados.
    Útil cuando necesitas buscar información actualizada, noticias o datos recientes."""
    try: 
        resultados=DDGS().text(query, max_results=1)
        texto_limpio="\n".join(f"URL: {res['href']}\nBody: {res['body']}"   for res in resultados )
        print(texto_limpio)
        return texto_limpio
    except Exception as e:
        return f"Error al buscar en Google: {e}"


def tool_llm():


    try:
        llm_gemini_instance = ChatOllama(
            model="qwen2.5",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
            repeat_penalty=1.15,
            #format="json"
            #num_gpu=1,
            #num_thread=12
        )
        print("Modelo llama3.1 (Ollama local) inicializado correctamente.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatOllama. Asegúrate de que Ollama esté corriendo. Mensaje: {e}")

    

    search_tool = {
        "title": "google_search",
        "description": "Returns about fresh events and news from Google Search engine based on a query",
        "type": "object",
        "properties": {
        "query": {
           "description": "Search query to be sent to the search engine",
           "title": "search_query",
           "type": "string"},
        },
        "required": ["query"]
        
    }

    # 2. Vinculamos de manera nativa la herramienta al modelo usando bind_tools
    llm_with_tools = llm_gemini_instance.bind_tools([google_search])


    result=llm_with_tools.invoke([HumanMessage(content="cuantos años tiene actualmente donald trump ")])
    texto=[]
    
    if hasattr(result, "tool_calls"):

        for tool_call in result.tool_calls:
            print("\n--- INSTANCIA DE LLAMADA DETECTADA ---")
            print(f"herramienta usa {tool_call['name']}")
            print(f"los argumentos son {tool_call['args']}")


            busqueda=google_search.invoke({"query": tool_call['args']['query']})

            print(f"\ Lo que encontró Python en internet:\n{busqueda}")


            resultado_final = llm_with_tools.invoke([
            HumanMessage(content=busqueda),
            ToolMessage(content=busqueda, tool_call_id=tool_call["id"])
            ])

        
    


    else:
        print("\n-NO SE LLAMÓ A LA HERRAMIENTA -")
        print("El modelo decidió responder con texto normal:")

        print(result.content)

    return result.tool_calls



    
    


if __name__ == "__main__":
    
   tool_llm()
