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
from typing import TypedDict
from langchain_classic.storage import LocalFileStore
from langchain_classic.embeddings import CacheBackedEmbeddings
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
# Configuración inicial de logs y warnings
load_dotenv(find_dotenv())



def crear_pdf_store_vectore(lista_documentos):


    logging.basicConfig(level=logging.ERROR)
    # Ruta LOCAL en C: — ChromaDB (Rust) no puede escribir en rutas de red (\\belenus\...)
    persistence_directory = r"C:\Users\afonseca\chroma_db"
    cache_directory = r"C:\Users\afonseca\embeddings_cache"



    try:
        embeddings_model = OllamaEmbeddings(
            model="bge-m3", 
            base_url="http://localhost:11434"
        )


        store=LocalFileStore(cache_directory)
        
        embedding_cache=CacheBackedEmbeddings.from_bytes_store(
            embeddings_model, 
            store, 
            namespace=embeddings_model.model
        )

        print(f"Cache embeddings inicializado en: {cache_directory}")

    except Exception as e:
        print(f"ERROR: Falló la inicialización de CacheBackedEmbeddings. Mensaje: {e}")
    

    text_splitter = SemanticChunker(
        embeddings=embeddings_model, # Le pasamos tu modelo de Ollama
        add_start_index=True
    )
    docs = text_splitter.split_documents(lista_documentos)
    print(f"Se han creado {len(docs)} chunks de texto.")


    logging.getLogger('chromadb').setLevel(logging.CRITICAL)
    #persistence_directory = "./chroma_db"
    if os.path.exists(persistence_directory):
        try:
            shutil.rmtree(persistence_directory)
            print(f"Carpeta '{persistence_directory}' eliminada para crear una nueva.")
            time.sleep(2)
        except Exception as e:
            print(f"ERROR: No se pudo eliminar la carpeta '{persistence_directory}'. Mensaje: {e}")
            

    vectorstore=Chroma.from_documents(
        documents=docs,
        embedding=embeddings_model,
        persist_directory=persistence_directory
    )

    #vectorstore.persist()
    print("el numero de vectores de la DB es:", vectorstore._collection.count())

    return vectorstore,docs





def definir_pregunt(question: str)-> str:

    try:
        llm_gemini_instance = ChatOllama(
            model="qwen2.5:14b",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
            repeat_penalty=1.15,
            #format="json"
            #num_gpu=1,
            #num_thread=12  
        )
        print("Modelos de Langchain para la pregunta incializado.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de llm para pregunta. Mensaje: {e}")


    expansion_template = expansion_template = """Dada la pregunta original del usuario: {question}

Tu objetivo es interpretar la intención subyacente del usuario y generar tres versiones alternativas de búsqueda para una base de datos vectorial. Debes capturar todos los contextos posibles del tema, desde lo más simple hasta lo más general.

Importante: Incluye en las busquedas palabras claves como: procedimientos y NOMBRES DE ARCHIVOS O DOCUMENTOS ANEXOS relacionados.
 
Reglas ESTRICTAS de generación:
- LÍNEA 1 (Directa y Simple): Reescribe la pregunta original de forma autocontenida, clara y directa, resolviendo cualquier ambigüedad.
- LÍNEA 2 (Abstracción Conceptual): Generaliza la intención. ¿Qué concepto más amplio, proceso, guía o documentación está buscando el usuario realmente? Formula una pregunta sobre ese marco general.
- LÍNEA 3 (Contexto y Sinónimos): Formula una pregunta utilizando jerga técnica, vocabulario alternativo o términos de negocio que los manuales o documentos oficiales podrían usar para explicar este tema.
- FORMATO: Las preguntas deben ser MUY cortas y precisas. Devuelve ÚNICAMENTE las tres preguntas, separadas por un salto de línea (sin números, sin viñetas y sin introducciones)."""


    expansion_prompt = PromptTemplate(
        input_variables=["question"],
        template=expansion_template
    )
    
    expansion_chain = expansion_prompt | llm_gemini_instance | StrOutputParser()

  
    resultado_texto = expansion_chain.invoke({"question": question})
    print(f"pregunta expandida: {resultado_texto}")
    print("finalizo modelo de pregunta")
    print('--------------------------------')

    return resultado_texto








def obtener_rag_chain(vector_store: Chroma,docs,pregunta_expandida):

    try:
        llm_gemini_instance = ChatOllama(
            model="gemma2:27b-instruct-q4_0",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
            num_ctx=2048,      # CRÍTICO: Limita el contexto máximo a 2048 tokens. Si es muy alto, colapsa la VRAM.
            num_gpu=-1,        # Le dice a Ollama que cargue la máxima cantidad de capas posibles en la GPU.
            num_thread=12
        )
        print("Modelo qwen2.5:14b (Ollama local) inicializado correctamente.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatOllama. Asegúrate de que Ollama esté corriendo. Mensaje: {e}")

    #parser_json = JsonOutputParser()
        

    """
    Returns:
        RetrievalQA: La cadena RAG configurada.
        
    """

    custom_prompt_template = """Lee cuidadosamente el siguiente documento corporativo.

<contexto>
{context}
</contexto>

---
Eres un Auditor Forense de Datos. Tu trabajo depende de tu precisión. Basándote EXCLUSIVAMENTE en el contexto de arriba, responde a la pregunta del usuario cumpliendo estas REGLAS INQUEBRANTABLES:

1. CERO ALUCINACIONES: Si la información exacta para responder la pregunta no se encuentra en el contexto, di explícitamente "La información solicitada no se encuentra".
2. EXTRACCIÓN COMPLETA: Analiza la pregunta del usuario. Si pide múltiples datos (por ejemplo, tiempos, roles, o ubicaciones), asegúrate de extraer y responder a cada uno de ellos sin omitir partes.
3. FIDELIDAD: No asumas conocimientos externos. Usa las cifras y nombres exactos del documento.

Para obligarte a pensar paso a paso, DEBES imprimir tu respuesta con esta estructura exacta:

**ANALISIS :**
(Escribe aquí tu análisis: ¿Qué datos específicos está pidiendo el usuario? ¿En qué parte del contexto están?)

**RESPUESTA FINAL:**
(Escribe aquí tu respuesta final en viñetas, de forma clara y directa).
"""

    CUSTOM_PROMPT = ChatPromptTemplate.from_messages([
        ("system", custom_prompt_template),
        ("human", "{question}"), # RetrievalQA usa 'question' en lugar de 'input'
    ])


    vector_retriever = vector_store.as_retriever(
        search_type="mmr", # <-- ¡Aquí activamos MMR!
        search_kwargs={
            'k': 3,             # CRÍTICO: Bajar de 20 a solo 3 o 4 documentos.
        'fetch_k': 15,      # Buscar entre 15 antes de aplicar MMR.
        'lambda_mult': 0.5 # Parámetro de diversidad (0=máxima diversidad, 1=máxima relevancia)
        }
    )


    compressor = LLMChainExtractor.from_llm(llm_gemini_instance)

    compressor_retriever= ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vector_retriever # <-- El híbrido le entrega los documentos al compresor
    )

####################################################################################################################
    class EstadoRAG(TypedDict):
        pregunta: str
        docs: list                
        respuesta_final: str
        reporte_problemas: str   
        hay_problemas: bool
        

    def nodo_recuperacion(state:EstadoRAG):
        pregunta_actual=state['pregunta']
        docs=compressor_retriever.invoke(pregunta_actual)
        return {'docs':docs}
    

    def generar_respuesta(state:EstadoRAG):
        docs_content="\n\n".join([doc.page_content for doc in state['docs']])

        messages=CUSTOM_PROMPT.format_messages(
            context=docs_content,
            question=state['pregunta']
        )

        respuesta=llm_gemini_instance.invoke(messages).content
        return {'respuesta_final': respuesta}


    def doble_check(state:EstadoRAG):

        respuesta_previa = state.get('respuesta_final', '')

        result= llm_gemini_instance.invoke(
             [
                {
                    "role": "user",
                "content": (
                    "Revisa la siguiente respuesta generada para comprobar si cumple "
                    "con nuestros estándares corporativos de auditoría.\n"
                    "Devuelve 'PROBLEMAS ENCONTRADOS' seguido de cualquier problema detectado "
                    "o devuelve 'SIN PROBLEMAS' si todo está correcto:\n\n"
                    f"{respuesta_previa}"
                    )
                }
            ]
        ).content

        if "PROBLEMAS ENCONTRADOS" in result:
            print("Problemas encontrados en la respuesta")
            return {
                "reporte_problemas": result.split("PROBLEMAS ENCONTRADOS", 1)[-1].strip(),
                "hay_problemas": True
                }   



        print(" Respuesta aprobada por el supervisor.")
        return {
            "reporte_problemas": "",
            "hay_problemas": False
        }


    def redactor_final(state:EstadoRAG):


        if state.get("hay_problemas")==True:
            print("Corrigiendo la respuesta basándose en el reporte del supervisor...")

            respuesta_corregida=llm_gemini_instance.invoke(
            [
                {
                    "role": "user",
                    "content": (
                        f"Reescribe la siguiente respuesta para solucionar estos errores detectados: {state['reporte_problemas']}\n\n"
                        f"Respuesta Original: {state['respuesta_final']}\n\n"
                        "Devuelve ÚNICAMENTE la respuesta corregida completa, sin introducciones."
                    )   
                }
            ]
        ).content

            return {"respuesta_final": respuesta_corregida}
    
        print(" No hay correcciones que hacer. Enviando respuesta original.")
        return {}

####################################################################################################################
    
################LANGRAPH #######################

    graph_builder=StateGraph(EstadoRAG)
    graph_builder.add_node("recuperar", nodo_recuperacion)
    graph_builder.add_node("generar", generar_respuesta)
    graph_builder.add_node("verificar", doble_check)
    graph_builder.add_node("corregir", redactor_final)

    graph_builder.add_edge(START, "recuperar")
    graph_builder.add_edge("recuperar", "generar")
    graph_builder.add_edge("generar", "verificar")

    def decidir_ruta(state: EstadoRAG):
        if state.get("hay_problemas") == True:
            return "corregir"
        return END
    
    graph_builder.add_conditional_edges(
    "verificar",
    decidir_ruta
)

    graph_builder.add_edge("corregir", END)
    app_agente = graph_builder.compile()


    ####################################################################################################################
    estado_inicial = {
        "pregunta": pregunta_expandida,
        "docs": [],
        "respuesta_final": "",
        "reporte_problemas": "",
        "hay_problemas": False
    }

    print("\n🚀 EJECUTANDO AGENTE LANGGRAPH...")
    # Invocamos el agente (Esto pone todo a rodar)
    resultado_final = app_agente.invoke(estado_inicial)

    # Devolvemos SÓLO el string con la respuesta final a Streamlit
    return resultado_final['respuesta_final']
