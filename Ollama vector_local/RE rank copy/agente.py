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
#from langchain.output_parsers import JsonOutputParser

from langchain_core.runnables import RunnableLambda
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain



# Configuración inicial de logs y warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)
load_dotenv(find_dotenv())



# no se usa por ahora
def deduplicar_contexto(documentos: list[Document]) -> list[Document]:

    lineas_unicas=[]
    texto_visto=set()
    x
    for doc in documentos:
        lineas_actuales=len(doc.page_content.split('\n'))
        lineas_unicas.extend(doc.page_content.split('\n'))
        for linea in doc.page_content.split('\n'):
            if linea in texto_visto:
                lineas_unicas.remove(linea)
            else:
                texto_visto.add(linea)

    texto_consolidado="\n".join(lineas_unicas)
    return Document(page_content=texto_consolidado)
    

def crear_pdf_store_vectore(lista_documentos):
    
    try:
        embeddings_model = OllamaEmbeddings(
            model="nomic-embed-text", 
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

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=2000,  # Un tamaño más realista para modelos de lenguaj
        chunk_overlap=500, # Se asegura de que cada fragmento se superponga con el siguiente en 200 caracteres.
        
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
    #vectorstore.persist()

    return vectorstore,docs







def obtener_rag_chain(vector_store: Chroma,docs):


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
        print("Modelo Qwen 2.5 14B (Ollama local) inicializado correctamente.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatOllama. Asegúrate de que Ollama esté corriendo. Mensaje: {e}")

    #parser_json = JsonOutputParser()
        

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

    **REGLAS DE CONSOLIDACIÓN ESTRICTA:**
    1. Analiza todo el contexto antes de responder.
    2. Si encuentras entidades, empresas, contactos o datos que se repiten en diferentes partes del texto, CONSOLÍDALOS.
    3. NUNCA repitas la misma información, el mismo contacto o la misma empresa dos veces en tu respuesta final. Agrúpalos lógicamente.


    ¿Listo para que exploremos juntos?

    Contexto:
    {context}

    Pregunta:
    {question}

    Respuesta:
    """
    CUSTOM_PROMPT = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])


#######  Advanced RAG (Retrieval-Augmented Generation Avanzado). #######################

    vector_retriever = vector_store.as_retriever(
        search_type="mmr", # <-- ¡Aquí activamos MMR!
        search_kwargs={
            'k': 10,            # Número de documentos a devolver 
            'fetch_k': 25,     # Número de documentos a recuperar inicialmente
            'lambda_mult': 0.5 # Parámetro de diversidad (0=máxima diversidad, 1=máxima relevancia)
        }
    )


    compressor = LLMChainExtractor.from_llm(llm_gemini_instance)

    compressor_retriever= ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vector_retriever # <-- El híbrido le entrega los documentos al compresor
    )
        
    
    ###################Advanced RAG (Retrieval-Augmented Generation Avanzado). ###########################################
    ################   #####################################


    qa_chain = RetrievalQA.from_chain_type(
            llm=llm_gemini_instance, # Usamos la variable local de la función
            retriever=compressor_retriever, # <-- Pasamos el orquestador híbrido
            chain_type_kwargs={"prompt": CUSTOM_PROMPT},
            chain_type="stuff"
        )

        # utilizar el Query transformation: Improving retrieval through better queries para realizar mas preguntas de la misma
    result = qa_chain.invoke("Según el documento, si necesito reportar una falla en las comunicaciones directamente a la empresa Tigo, ¿a qué dirección de correo electrónico debo escribir, y qué anomalía notas en esa información?")
        #results = qa_chain({'query': 'Who is the CV about?'}) # the other way of doing the same thing
    print(result['result'])

    return result['result']


