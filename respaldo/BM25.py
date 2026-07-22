import os
import shutil
import warnings
import logging
# from dotenv import find_dotenv, load_dotenv # Puedes comentar esta línea si ya no la usas en este archivo
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai
import asyncio
from langchain_community.document_loaders import PyPDFLoader
#Configuración inicial de logs y warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)
from dotenv import find_dotenv, load_dotenv
import os
import asyncio
import warnings
import logging
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
import logging
import streamlit as st
from langchain_cohere import CohereEmbeddings
import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter
import re
# 1. El orquestador que une ambas búsquedas
from langchain_classic.retrievers import EnsembleRetriever

# 2. El buscador por palabras clave (Búsqueda Tradicional / Sparse)
from langchain_community.retrievers import BM25Retriever

# 3. La base de datos vectorial para buscar por significado (Búsqueda Semántica / Dense)
from langchain_community.vectorstores import FAISS

load_dotenv(find_dotenv())


try:
        llm_gemini_instance = GoogleGenerativeAI(model="gemini-2.5-flash")
        embeddings_model_instance = CohereEmbeddings(model="embed-multilingual-v3.0")
        print("Modelos de Langchain (LLM y Embeddings) inicializados en rag_system.")
        

except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatGoogleGenerativeAI o GoogleGenerativeAIEmbeddings. Mensaje: {e}")
        print("Asegúrate de que los nombres de los modelos sean correctos y que la API Key tenga acceso a ellos.")
        
full_path = r"w:\ComandosSQL\sql scripts-Esteban\LL R\chat bot-12\data_2.pdf"
test_persistence_dir = "./chroma_db"



import re

@st.cache_data()
def limpiar_markdown(_documentos: list):
    doc_limpios = []
    for doc in _documentos:
        texto_md = doc.page_content
        # 1. Eliminar encabezados y pies de página recurrentes
        texto_md = re.sub(r'SGCA03T[^\n]*13/12/2023', '', texto_md)
        texto_md = re.sub(r'CELSA', '', texto_md)
        texto_md = re.sub(r'Página No\. \d+', '', texto_md)
        texto_md = re.sub(r'FIN DEL DOCUMENTO', '', texto_md)
        texto_md = re.sub(r'[ \t]{2,}', ' ', texto_md)
        texto_md = re.sub(r'\n{3,}', '\n\n', texto_md)
        texto_md = re.sub(r'^\|[-: |]+\|$', '', texto_md, flags=re.MULTILINE)
        texto_md = texto_md.replace('|', ' ')
        # 5. Eliminar etiquetas de imágenes en Markdown (ej: ![imagen](ruta.png))
        # Para que los logos y gráficos no ensucien los vectores de texto.
        texto_md = re.sub(r'!\[.*?\]\(.*?\)', '', texto_md)
        
        from langchain_core.documents import Document
        new_doc = Document(page_content=texto_md.strip(), metadata=doc.metadata)
        doc_limpios.append(new_doc)
        
    return doc_limpios


def markdown (file_path: str):

    texto = pymupdf4llm.to_markdown(file_path)
    texto = texto.replace("SGCA03T", "").replace("V1_1", "")

    headers_to_split_on = [
    ("#", "Titulo Nivel 1"),
    ("##", "Titulo Nivel 2")
]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = markdown_splitter.split_text(texto)
    
    print("archivo cargado correctamente como split-markdown")

    return docs


# @st.cache_data()
# def load_docs(file_path: str):
     
#     extension = os.path.splitext(file_path)[1].lower() 
    

#     if extension == '.pdf':
#         loader = PyPDFLoader(file_path)
#     elif extension in ['.docx', '.doc']:
#         loader = Docx2txtLoader(file_path)
#     elif extension == '.txt':
#         loader = TextLoader(file_path)
#     else:
#         # Si el archivo no es de un tipo soportado, avisa y devuelve una lista vacía.
#         st.warning(f"El formato del archivo '{extension}' no es soportado.")
#         return []

#     # Carga y devuelve los documentos (como una lista)
#     return loader.load()

def guardar_markdown(texto: str, nombre_archivo: str):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)



def crear_pdf_store_vectore(lista_documentos,embeddings_model: CohereEmbeddings,persistence_directory: str):

    
    import logging
    logging.basicConfig(level=logging.ERROR)

    text_splitter = RecursiveCharacterTextSplitter(
        
        chunk_size=1000,  # Un tamaño más realista para modelos de lenguaj
        chunk_overlap=200, # Se asegura de que cada fragmento se superponga con el siguiente en 50 caracteres.
        
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
    return vectorstore







def obtener_rag_chain(llm_gemini: GoogleGenerativeAI, vector_store: Chroma, docs):
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


    vector_retriever = vector_store.as_retriever(search_kwargs={'k': 5})
    
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = 5



    hybrid_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.7, 0.3]
    )





    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_gemini, # Usamos la variable local de la función
        retriever=hybrid_retriever, # <-- Pasamos el orquestador híbrido
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},
        chain_type="stuff"
    )

    result = qa_chain("quien creo el documento o lo aprobo?")
    #results = qa_chain({'query': 'Who is the CV about?'}) # the other way of doing the same thing
    #print(result['result'])


    vector_retriever_2=bm25_retriever.invoke("quien creo el documento o lo aprobo?")

    for i,doc in enumerate(vector_retriever_2):
        print(f"chunk: {i+1}")
        print(doc.page_content[:300] + "...\n")
    return result['result']



documentos_cargados = limpiar_markdown(markdown(full_path))

texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
guardar_markdown(texto_completo, ruta_guardado)
print(f"Markdown guardado en: {ruta_guardado}")

vector_db = crear_pdf_store_vectore(documentos_cargados, embeddings_model_instance, test_persistence_dir)
qa_chain = obtener_rag_chain(llm_gemini_instance, vector_db, documentos_cargados)
