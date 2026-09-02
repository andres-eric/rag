

import os
import logging
from dotenv import find_dotenv, load_dotenv
from utils import limpiar_markdown, guardar_markdown
from agente import crear_pdf_store_vectore, obtener_rag_chain
import time

#logging.getLogger("streamlit").setLevel(logging.ERROR)
load_dotenv(find_dotenv())

print("tiempo de ejecución inicio")
tiempo_inicio_programa = time.perf_counter()

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
full_path = os.path.join(base_dir, "ti.pdf")
test_persistence_dir = r"C:\Users\afonseca\chroma_db"
documentos_cargados = limpiar_markdown(full_path)

texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
guardar_markdown(texto_completo, ruta_guardado)
print(f"Markdown guardado en: {ruta_guardado}")

inicio = time.perf_counter()
vector_db, chunks = crear_pdf_store_vectore(documentos_cargados)
fin = time.perf_counter()
#print(f"Tiempo transcurrido: {fin - inicio}")
qa_chain = obtener_rag_chain(vector_db, chunks)
minutos_llm=int(fin - inicio)//60
segundos_llm=round((fin - inicio)%60,2)
print(f"⏱️ Tiempo total: {minutos_llm}m {segundos_llm:.2f}s ({fin - inicio} segundos)")
fin_programa = time.perf_counter()
minutos_programa=int(fin_programa-tiempo_inicio_programa)//60
segundos_programa=round((fin_programa-tiempo_inicio_programa)%60,2)
print(f"⏱️ Tiempo total del programa: {minutos_programa}m {segundos_programa:.2f}s ({fin_programa-tiempo_inicio_programa} segundos)")

