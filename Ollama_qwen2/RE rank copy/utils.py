import os
import shutil
import warnings
import logging
import re

import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_cohere import CohereEmbeddings
from langchain_google_genai import GoogleGenerativeAI

# Configuración inicial de logs y warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)

load_dotenv(find_dotenv())


# Obtener la ruta base del proyecto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_path = os.path.join(base_dir, "data_2.pdf")





import re

@st.cache_data()

def limpiar_markdown(ruta_pdf: str):
    """
    Función maestra para Streamlit.
    Realiza la extracción, limpieza exhaustiva y división en chunks en el ORDEN CORRECTO.
    """

    texto_md = pymupdf4llm.to_markdown(ruta_pdf)
    
    
    
    # texto_md = re.sub(r'^.*?(?=(?:\#+\s*)?\**1\.\s*OBJETIVO\**)', '', texto_md, flags=re.DOTALL | re.IGNORECASE)


    texto_md = re.sub(r'SGCA03T[^\n]*13/12/2023', '', texto_md)
    texto_md = re.sub(r'CELSA', '', texto_md)
    texto_md = re.sub(r'Página No\. \d+', '', texto_md)
    texto_md = re.sub(r'\**\s*HOMOLOGACIÓN DE MATERIAS\s*PRIMAS\s*13/12/2023\**', '', texto_md)
    texto_md = re.sub(r'\**_*\s*FIN DEL DOCUMENTO\s*_*\**', '', texto_md)

    
    texto_md = re.sub(r'\.{4,}\s*\d*', '', texto_md)       # Borra "....... 3"
    texto_md = re.sub(r'<br\s*/?>', ' ', texto_md, flags=re.IGNORECASE)  # Borra <br>

    texto_md = re.sub(r'!\[.*?\]\(.*?\)', '', texto_md)    # Quita etiquetas de imágenes
    texto_md = re.sub(r'^[ \t]*\|[-:\s|]+\|[ \t]*$', '', texto_md, flags=re.MULTILINE) # Borra |---|---|
    texto_md = texto_md.replace('|', ' ')                  # Quita las barras verticales de las columnas


    texto_md = re.sub(r'[ \t]{2,}', ' ', texto_md)
    texto_md = re.sub(r'\n{3,}', '\n\n', texto_md)
    texto_md = texto_md.strip()


    headers_to_split_on = [
        ("#", "Titulo Nivel 1"),
        ("##", "Titulo Nivel 2"),
        ("###", "Titulo Nivel 3")
    ]
    
    #MarkdownTextSplitter divisor especializado para datos que estan en markdonw
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    # Esto automáticamente procesa el string y devuelve una LISTA de objetos 'Document'
    documentos_finales = markdown_splitter.split_text(texto_md)
    
    return documentos_finales



def guardar_markdown(texto: str, nombre_archivo: str):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)


# documentos_cargados= limpiar_markdown(full_path)
# texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
# ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
# guardar_markdown(texto_completo, ruta_guardado)
# print(f"Markdown guardado en: {ruta_guardado}")







