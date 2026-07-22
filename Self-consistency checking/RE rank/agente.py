import os
import re
import shutil
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import logging
import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAI
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.output_parsers import JsonOutputParser
# Configuración inicial de logs
logging.basicConfig(level=logging.ERROR)
load_dotenv(find_dotenv())


def crear_pdf_store_vectore(lista_documentos):
    try:
        embeddings_model = CohereEmbeddings(model="embed-multilingual-v3.0")
        print("Modelos de Langchain (Embeddings) inicializados en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de CohereEmbeddings. Mensaje: {e}")
        print("Asegúrate de que los nombres de los modelos sean correctos y que la API Key tenga acceso a ellos.")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir.startswith(("\\\\", "//")):
        import tempfile
        persistence_directory = os.path.join(tempfile.gettempdir(), "chroma_db_self_consistency")
    else:
        persistence_directory = os.path.join(base_dir, "chroma_db")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(lista_documentos)
    print(f"Se han creado {len(docs)} chunks de texto.")

    logging.getLogger('chromadb').setLevel(logging.CRITICAL)
    if os.path.exists(persistence_directory):
        try:
            shutil.rmtree(persistence_directory, ignore_errors=True)
            print(f"Carpeta '{persistence_directory}' eliminada para crear una nueva.")
        except Exception as e:
            print(f"No se pudo eliminar '{persistence_directory}': {e}")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings_model,
        persist_directory=persistence_directory
    )

    return vectorstore, docs


def definir_pregunt(question: str) -> str:
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
    resultado_texto = expansion_chain.invoke({"question": question})

    return resultado_texto


class RAGChainWrapper:
    def __init__(self, qa_chain):
        self.qa_chain = qa_chain
        
    def invoke(self, inputs):
        query = inputs.get("query")
        pregunta_mejorada = definir_pregunt(query)
        print("pregunta_mejorada::  ", pregunta_mejorada)
        result = self.qa_chain.invoke(pregunta_mejorada)
        return result


def obtener_rag_chain(vector_store: Chroma, docs):

    try:
        llm_gemini_instance = GoogleGenerativeAI(model="gemini-2.5-flash")
        print("Modelos de Langchain (LLM) inicializado en rag_system.")
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatGoogleGenerativeAI. Mensaje: {e}")
        

    """
    Returns:
        RAGChainWrapper: La cadena RAG configurada envuelta.
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

    vector_retriever = vector_store.as_retriever(search_kwargs={'k': 5})
    
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
        chain_type="stuff",
        return_source_documents=True
        
    )

    return RAGChainWrapper(qa_chain)



def verificar_response_acuracy(
    retrieved_docs: list[Document],
    answer: str,
    llm: GoogleGenerativeAI=None
) -> dict:
    """
    Verify if a generated answer is fully supported by the retrieved documents.
    Args:
        retrieved_docs: List of documents used to generate the answer
        answer: The answer produced by the RAG system
        llm: Language model to use for verification
    Returns:
        Dictionary containing verification results and any identified issues
    """
    if llm is None:
        llm = GoogleGenerativeAI(model="gemini-2.5-flash")
        
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    verification_prompt = ChatPromptTemplate.from_template("""
    As a fact-checking assistant, verify whether the following answer is 
fully supported
    by the provided context. Identify any statements that are not 
supported or contradict the context.
    Context:
    {context}
    Answer to verify:
    {answer}
    Perform a detailed analysis with the following structure:
    1. List any factual claims in the answer
    2. For each claim, indicate whether it is:
       - Fully supported (provide the supporting text from context)
       - Partially supported (explain what parts lack support)
       - Contradicted (identify the contradiction)
       - Not mentioned in context
    3. Overall assessment: Is the answer fully grounded in the context?
    Return your analysis in JSON format with the following structure:
    {{
      "claims": [
        {{
          "claim": "The factual claim",
          "status": "fully_supported|partially_supported|contradicted|not_mentioned",
          "evidence": "Supporting or contradicting text from context",
          "explanation": "Your explanation"
        }}
      ],
      "fully_grounded": true|false,
      "issues_identified": ["List any specific issues"]
    }}
    """)

    verification_chain = (verification_prompt | llm | StrOutputParser())
    result = verification_chain.invoke({"context": context, "answer": answer})

    
    return result
