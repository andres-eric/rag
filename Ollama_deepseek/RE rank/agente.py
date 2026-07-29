import os
import re
import shutil
import warnings
import logging
import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank



# Configuración inicial de logs y warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)
load_dotenv(find_dotenv())



def crear_pdf_store_vectore(lista_documentos):
    
    try:
        embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
        print("Modelos de Langchain (Embeddings) inicializados en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de CohereEmbeddings. Mensaje: {e}")
        print("Asegúrate de que los nombres de los modelos sean correctos y que la API Key tenga acceso a ellos.")
    

    
    import logging
    logging.basicConfig(level=logging.ERROR)
    # Ruta LOCAL en C: — ChromaDB (Rust) no puede escribir en rutas de red (\\belenus\...)
    persistence_directory = r"C:\Users\afonseca\chroma_db"



    #SemanticChunker divide segun la idea de la lectura

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,  # Un tamaño más realista para modelos de lenguaj
        chunk_overlap=200, # Se asegura de que cada fragmento se superponga con el siguiente en 200 caracteres.
        
    )
    docs = text_splitter.split_documents(lista_documentos)
    print(f"Se han creado {len(docs)} chunks de texto.")


    logging.getLogger('chromadb').setLevel(logging.CRITICAL)
    #persistence_directory = "./chroma_db"
    if os.path.exists(persistence_directory):
        shutil.rmtree(persistence_directory)
        print(f"Carpeta '{persistence_directory}' eliminada para crear una nueva.")

    vectorstore=Chroma.from_documents(
        documents=docs,
        embedding=embeddings_model,
        persist_directory=persistence_directory
    )
    vectorstore.persist()

    return vectorstore,docs







def obtener_rag_chain(vector_store: Chroma,docs):


    try:
        llm_gemini_instance = ChatOllama(
            model="deepseek-r1:1.5b",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.3,
        )
        print("Modelo DeepSeek R1 1.5b (Ollama local) inicializado correctamente.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatOllama. Asegúrate de que Ollama esté corriendo. Mensaje: {e}")
        

    """
    Returns:
        RetrievalQA: La cadena RAG configurada.
    """

    custom_prompt_template = """
    ¡Hola! Estoy aquí para ayudarte a explorar y entender la información que me has proporcionado. Me encargaré de revisar el contexto **con mucho cuidado** para darte una respuesta **completa, y fácil de entender**.
    si el documento es tecnico la idea debe ser faci de entender por favor que la respuesta este en ESPAÑOL

    Mi misión es desglosar la información para ti, asegurándome de extraer los detalles más importantes y específicos. Esto incluye:
    * **Nombres y personas relevantes.**
    * **Fechas clave y periodos de tiempo.**
    * **Cifras, estadísticas y cualquier dato numérico preciso.**
    * **Términos técnicos o detalles específicos** que sean importantes para tu pregunta.

    Si la respuesta que necesitas involucra varios puntos o una lista, la organizaré en **viñetas o una numeración clara** para que te sea muy sencillo seguirla.

    **Una cosa importante:** Si, después de buscar exhaustivamente en el texto, no encuentro la respuesta o el detalle específico que pides, te lo haré saber honestamente. Simplemente te diré: "La información solicitada no se encuentra en el documento proporcionado." ¡No me inventaré nada! Mi prioridad es darte solo información que esté **explícitamente** en el documento.

    ¿Listo para que exploremos juntos?

    Contexto:
    {context}

    Pregunta:
    {question}

    Respuesta:
    """
    CUSTOM_PROMPT = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])


#######  Advanced RAG (Retrieval-Augmented Generation Avanzado). #######################


    vector_retriever = vector_store.as_retriever(search_kwargs={'k': 5})
    
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = 10



    hybrid_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.7, 0.3]
    )

    
    compressor = CohereRerank(
        model="rerank-multilingual-v3.0",
        top_n=3)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=hybrid_retriever # <-- El híbrido le entrega los documentos al compresor
    )


###################Advanced RAG (Retrieval-Augmented Generation Avanzado). ###########################################
################   #####################################


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_gemini_instance, # DeepSeek R1 1.5b via Ollama local
        retriever=compression_retriever, # <-- Pasamos el orquestador híbrido
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},
        chain_type="stuff"
    )


    result = qa_chain.invoke("dame un resumen del documento?")
    #results = qa_chain({'query': 'Who is the CV about?'}) # the other way of doing the same thing
    print(result['result'])

    return result['result']


