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


load_dotenv(find_dotenv())


try:
        llm_gemini_instance = GoogleGenerativeAI(model="gemini-2.5-flash")
        embeddings_model_instance = CohereEmbeddings(model="embed-multilingual-v3.0")
        print("Modelos de Langchain (LLM y Embeddings) inicializados en rag_system.")
        

except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatGoogleGenerativeAI o GoogleGenerativeAIEmbeddings. Mensaje: {e}")
        print("Asegúrate de que los nombres de los modelos sean correctos y que la API Key tenga acceso a ellos.")
        
full_path = r"C:\Users\afonseca\Desktop\langchain\chat bot-12\data_2.pdf"
test_persistence_dir = "./chroma_db"



@st.cache_data()
def load_docs(file_path: str):
     
    extension = os.path.splitext(file_path)[1].lower() 
    

    if extension == '.pdf':
        loader = PyPDFLoader(file_path)
    elif extension in ['.docx', '.doc']:
        loader = Docx2txtLoader(file_path)
    elif extension == '.txt':
        loader = TextLoader(file_path)
    else:
        # Si el archivo no es de un tipo soportado, avisa y devuelve una lista vacía.
        st.warning(f"El formato del archivo '{extension}' no es soportado.")
        return []

    # Carga y devuelve los documentos (como una lista)
    return loader.load()






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







def obtener_rag_chain(llm_gemini: GoogleGenerativeAI, vector_store: Chroma):
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

    qa_chain = RetrievalQA.from_chain_type(
        llm_gemini_instance,
        retriever=vector_store.as_retriever(search_kwargs={'k':7}),
        #return_source_documents=True,
        #verbose=True, # Puedes cambiar a False si no quieres ver el log detallado
        #return_source_documents=True,

    # 5. LA PLANTILLA (El destino del contexto):
    # Aquí le pasamos tu CUSTOM_PROMPT. LangChain buscará obligatoriamente 
    # la etiqueta {context} dentro de esa plantilla de texto para saber 
    # en qué línea exacta debe inyectar la información.
    # esta parte solo llena el contexto
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},


        # 6. LA ESTRATEGIA (El creador del contexto):
        # "stuff" es un motor interno que hace el trabajo sucio. Toma los 7 
        # fragmentos del retriever, los junta en un solo bloque de texto, 
        # los guarda en una variable oculta llamada exactamente 'context', 
        # y los envía directamente a la plantilla que definimos arriba.
        chain_type="stuff"
    )


    result = qa_chain("quien creo el documento o lo aprobo?")
    #results = qa_chain({'query': 'Who is the CV about?'}) # the other way of doing the same thing
    print(result['result'])

    return result['result']



documentos_cargados = load_docs(full_path)
vector_db = crear_pdf_store_vectore(documentos_cargados, embeddings_model_instance, test_persistence_dir)
qa_chain = obtener_rag_chain(llm_gemini_instance, vector_db)
    



