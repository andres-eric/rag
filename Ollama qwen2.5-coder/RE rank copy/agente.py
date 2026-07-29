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


# Configuración inicial de logs y warnings
load_dotenv(find_dotenv())



# no se usa por ahora
# def deduplicar_contexto(documentos: list[Document]) -> list[Document]:

#     lineas_unicas=[]
#     texto_visto=set()
#     for doc in documentos:
#         lineas_actuales=len(doc.page_content.split('\n'))
#         lineas_unicas.extend(doc.page_content.split('\n'))
#         for linea in doc.page_content.split('\n'):
#             if linea in texto_visto:
#                 lineas_unicas.remove(linea)
#             else:
#                 texto_visto.add(linea)

#     texto_consolidado="\n".join(lineas_unicas)
#     return Document(page_content=texto_consolidado)
    

def crear_pdf_store_vectore(lista_documentos):
    
    try:
        embeddings_model = OllamaEmbeddings(
            model="bge-m3", 
            base_url="http://localhost:11434"
        )

        print("Modelos de Langchain (Embeddings) inicializados en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de CohereEmbeddings. Mensaje: {e}")
        print("Asegúrate de que los nombres de los modelos sean correctos y que la API Key tenga acceso a ellos.")
    

    
    import logging
    logging.basicConfig(level=logging.ERROR)
    # Ruta LOCAL en C: — ChromaDB (Rust) no puede escribir en rutas de red (\\belenus\...)
    persistence_directory = r"C:\Users\afonseca\chroma_db"



    #SemanticChunker divide segun la idea de la lectura

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
            model="qwen2.5-coder:14b",
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

    # 4. Ejecutamos la cadena
    resultado_texto = expansion_chain.invoke({"question": question})
    print(f"pregunta expandida: {resultado_texto}")
    print("finalizo modelo de pregunta")
    print('--------------------------------')


    return resultado_texto








def obtener_rag_chain(vector_store: Chroma,docs,pregunta_expandida):


    try:
        llm_gemini_instance = ChatOllama(
            model="qwen2.5-coder:14b",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
            repeat_penalty=1.15,
            #format="json"
            #num_gpu=1,
            #num_thread=12
        )
        print("Modelo qwen2.5-coder:14b (Ollama local) inicializado correctamente.")
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


#######  Advanced RAG (Retrieval-Augmented Generation Avanzado). #######################

    vector_retriever = vector_store.as_retriever(
        search_type="mmr", # <-- ¡Aquí activamos MMR!
        search_kwargs={
            'k': 20,            # Número de documentos a devolver 
            'fetch_k': 60,     # Número de documentos a recuperar inicialmente
            'lambda_mult': 0.4 # Parámetro de diversidad (0=máxima diversidad, 1=máxima relevancia)
        }
    )


    compressor = LLMChainExtractor.from_llm(llm_gemini_instance)

    compressor_retriever= ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vector_retriever # <-- El híbrido le entrega los documentos al compresor
    )
    

    # sub_query_prompt=PromptTemplate(
    #     input_variables=["question"],
    #     template="""Eres un asistente experto en bases de datos vectoriales. Tu tarea es generar 3 versiones diferentes de la pregunta del usuario para recuperar documentos de una base de datos técnica de TI. 
    # Asegúrate de separar conceptos. Por ejemplo, si preguntan por 'servidores y backups', haz una pregunta sobre servidores y otra sobre políticas de backup.
    
    # Pregunta original: {question}
    # """
    # )

    # advanced_retriever = MultiQueryRetriever.from_llm(
    # retriever=compressor_retriever,
    # llm=llm_gemini_instance, # Usamos tu Qwen 2.5 local
    # prompt=sub_query_prompt
    # )
    
    ###################Advanced RAG (Retrieval-Augmented Generation Avanzado). ###########################################
    ################   #####################################
    # 1. Ensamblamos las cadenas (esto ya lo tienes bien)
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm_gemini_instance, # Usamos la variable local de la función
        retriever=compressor_retriever, # <-- Pasamos el orquestador híbrido
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},
        chain_type="stuff",
        return_source_documents=True
    )

    

    # 2. LA CORRECCIÓN: Invocamos rag_chain y le pasamos un diccionario con la llave "query"
    result = rag_chain.invoke({"query": pregunta_expandida})

    # 3. Iteramos sobre los documentos recuperados (en LCEL la llave es 'context')
    print("\n" + "="*50)
    print("📄 FRAGMENTOS LEÍDOS")
    print("="*50)
    for i, doc in enumerate(result.get('source_documents', [])):
        print(f"\n--- FUENTE {i+1} ---")
        print(f"Contenido:\n{doc.page_content}")
        print("-" * 20)

    # 4. Imprimimos la respuesta final (en LCEL la llave es 'answer')
    #print(f"pregunca: {consulta}")
    print("\n" + "="*50)
    print("🤖 RESPUESTA FINAL DEL AGENTE FORENSE")
    print("="*50)
    print(result.get('result', ''))
    # print(f"pregunca: {consulta}")
    # print('--------------------------------')
    # print(result['answer'])

    return result['result']
