import os
import re
import shutil
import warnings
import logging
import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

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
    persistence_directory = "./chroma_db"



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




######  tecnica para cuando los usuarios no usan el mismo lenguaje que el texto ############



def definir_pregunt(question: str)-> list[str]:


    try:
        llm_expansor = GoogleGenerativeAI(model="gemini-2.5-flash")
        print("Modelos de Langchain (LLM) inicializado en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatGoogleGenerativeAI. Mensaje: {e}")


    expansion_template = """Dada la pregunta original del usuario: {question}
    
Tu tarea es reescribir esta consulta en una ÚNICA pregunta que sea extremadamente clara, explícita y optimizada para que un motor de búsqueda vectorial o un LLM la entienda a la perfección.
    
Reglas ESTRICTAS:
- CONSERVA LA INTENCIÓN ORIGINAL: No te desvíes del tema central, no agregues conceptos nuevos y no asumas cosas que el usuario no preguntó.
- Genera solo UNA pregunta.
- Hazla completamente autocontenida (elimina pronombres vagos como "él", "eso", y reemplázalos por el sujeto real).
- Aclara la terminología técnica solo si ayuda a la búsqueda, pero manteniendo el límite de la pregunta inicial.
- Devuelve ÚNICAMENTE la pregunta reescrita, sin introducciones, sin comillas y sin explicaciones adicionales.
"""

    expansion_prompt = PromptTemplate(
        input_variables=["question"],
        template=expansion_template
    )
    
    expansion_chain = expansion_prompt | llm_expansor | StrOutputParser()

    # 4. Ejecutamos la cadena
    resultado_texto = expansion_chain.invoke({"question": question})

    return resultado_texto







######  tecnica para cuando los usuarios no usan el mismo lenguaje que el texto ############




def obtener_rag_chain(vector_store: Chroma,docs,question):


    try:
        llm_gemini_instance = GoogleGenerativeAI(model="gemini-2.5-flash")
        print("Modelos de Langchain (LLM) inicializado en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatGoogleGenerativeAI. Mensaje: {e}")
        

    """
    Returns:
        RetrievalQA: La cadena RAG configurada.
    """

    custom_prompt_template = """
    ¡Hola! Estoy aquí para ayudarte a explorar y entender la información que me has proporcionado. Me encargaré de revisar el contexto **con mucho cuidado** para darte una respuesta **completa, y fácil de entender**.
    si el documento es tecnico la idea debe ser faci de entender

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
################   #####################################


#Otro enfoque poderoso es la Relevancia Marginal Máxima (MMR), que equilibra la relevancia del documento 
#con la diversidad, asegurando que el conjunto recuperado contenga perspectivas variadas en lugar de 
#información redundante

    vector_retriever = vector_store.as_retriever(
    search_type="mmr", # <-- ¡Aquí activamos MMR!
    search_kwargs={
        'k': 5,            # Número de documentos a devolver al compresor
        'fetch_k': 20,     # Número de documentos a recuperar inicialmente
        'lambda_mult': 0.5 # Parámetro de diversidad (0=máxima diversidad, 1=máxima relevancia)
    }
)
    
   
###################Advanced RAG (Retrieval-Augmented Generation Avanzado). ###########################################
################   #####################################


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_gemini_instance, # Usamos la variable local de la función
        retriever=vector_retriever, # <-- Pasamos el orquestador híbrido
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},
        chain_type="stuff"
    )


    pregunta_mejorada= definir_pregunt(question)
    print("pregunta_mejorada::  ",pregunta_mejorada)
    # utilizar el Query transformation: Improving retrieval through better queries para realizar mas preguntas de la misma
    result = qa_chain.invoke(pregunta_mejorada)
    #results = qa_chain({'query': 'Who is the CV about?'}) # the other way of doing the same thing
    print(result['result'])

    return result['result']


### otra forma de generar una pregunta de forma eficiente es leyendo primero el documento y 
### despues contextualizando con la pregunta original del usuario y lo que esta en el documento pagina 144
### 
