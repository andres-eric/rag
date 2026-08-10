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
from langchain.messages import HumanMessage, ToolMessage, SystemMessage

import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

load_dotenv(find_dotenv())




@tool
def google_search(query:str)->str:
    """Busca en internet usando DuckDuckGo Search y devuelve los resultados.
    Útil cuando necesitas buscar información actualizada, noticias o datos recientes."""
    try: 
        resultados=DDGS().text(query, max_results=3)
        texto_limpio="\n".join(f"Link de la noticia: {res['href']}\nNoticia: {res['body']}"   for res in resultados )
        #print(texto_limpio)
        return texto_limpio
    except Exception as e:
        return f"Error al buscar en Google: {e}"

@tool
def caculadora_de_raices(numero:float)->float:
    """Calcula la raíz cuadrada de un número."""

    raiz=numero**0.5
    if raiz>0:
        return raiz
    else:
        raise ValueError("El número complejo no se puede calcular")
    

def tool_llm():


    try:
        llm_gemini_instance = ChatOllama(
            model="llama3.1",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
            #repeat_penalty=1.15,
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


    instrucciones_analista = SystemMessage(content=""""
    Eres un analista Senior de Licitaciones B2B para una empresa de energía renovable.
    Acabas de recibir los resultados de búsqueda en internet sobre licitaciones de paneles solares.

    REGLAS DE ANÁLISIS:
    1. Extrae únicamente las licitaciones que sean de Colombia.
    2. Descarta cualquier noticia que sea solo informativa (buscamos contratos o compras reales).
    3. Si el texto de internet viene basura o código, ignóralo y extrae solo lo legible.

    FORMATO DE RESPUESTA ESTRICTO:
    Para cada oportunidad válida, responde usando exactamente esta estructura:
    🔸 ENTIDAD: [Nombre de la entidad, ej: Alcaldía de Bogotá]
    🔸 DESCRIPCIÓN: [Resumen de 2 líneas de lo que se va a comprar]
    🔸 EVALUACIÓN COMERCIAL: [Por qué deberíamos participar en esto]
    🔸 LINK: https://www.youtube.com/watch?v=vw0m43ixSBs
    """)




    pregunta=HumanMessage(content="traeme licitaciones que tenga el estado colombiano o contrataciones acerca de paneles solares")

    mensaje=[instrucciones_analista,pregunta]

    result=llm_with_tools.invoke(mensaje)

    mensaje.append(result)

    if hasattr(result, "tool_calls") and len(result.tool_calls) > 0:

        for tool_call in result.tool_calls:
            print("\n--- INSTANCIA DE LLAMADA DETECTADA ---")
            print("######################################")
            #print(f"herramienta usa {tool_call['name']}")
            #print(f"los argumentos son {tool_call['args']}")

            # 1. Ejecutamos la herramienta para obtener la búsqueda
            busqueda=google_search.invoke({"query": tool_call['args']['query']})

            # 2. Iteramos cada noticia obtenida del resultado de la herramienta
            noticias = busqueda.split("Link de la noticia: ")
            conteo = 0
            for noticia in noticias:
                if noticia.strip():
                    print(f"--- Noticia número {conteo} ---")
                    print(f"Link de la noticia: {noticia.strip()}\n")
                    conteo += 1

            mensaje_herramienta = ToolMessage(content=busqueda, tool_call_id=tool_call["id"])
            mensaje.append(mensaje_herramienta)

            print(f"\n---MODELO ANALIZANDO LOS DATOS ---")

            resultado_final=llm_with_tools.invoke(mensaje)
            
            print("\n--- RESPUESTA FINAL DEL MODELO ---")
            print(resultado_final.content)

    else:
        print("\n-NO SE LLAMÓ A LA HERRAMIENTA -")
        print("El modelo decidió responder con texto normal:")

        print(result.content)

    return result.tool_calls



if __name__ == "__main__":
   tool_llm()
