import os
import logging
from dotenv import find_dotenv, load_dotenv
from utils import limpiar_markdown, guardar_markdown
from agente import crear_pdf_store_vectore, obtener_rag_chain


#logging.getLogger("streamlit").setLevel(logging.ERROR)
load_dotenv(find_dotenv())

# Obtener la ruta base del proyecto (un nivel arriba del directorio del script)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_path = os.path.join(base_dir, "ti.pdf")
test_persistence_dir = "./chroma_db"
documentos_cargados = limpiar_markdown(full_path)

texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
guardar_markdown(texto_completo, ruta_guardado)
print(f"Markdown guardado en: {ruta_guardado}")

question="Cómo funciona el esquema de comunicaciones de la empresa para evitar quedarse sin internet?"


vector_db, chunks = crear_pdf_store_vectore(documentos_cargados)
qa_chain = obtener_rag_chain(vector_db, chunks,question)
