import os
import logging
from dotenv import find_dotenv, load_dotenv
from utils import limpiar_markdown, guardar_markdown
from agente import crear_pdf_store_vectore, verificar_response_acuracy, obtener_rag_chain

#logging.getLogger("streamlit").setLevel(logging.ERROR)
load_dotenv(find_dotenv())

# Obtener la ruta base del proyecto (tres niveles arriba de donde está main.py, es decir, el root del workspace)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
full_path = os.path.join(base_dir, "ti.pdf")
test_persistence_dir = "./chroma_db"
documentos_cargados = limpiar_markdown(full_path)

texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
guardar_markdown(texto_completo, ruta_guardado)
print(f"Markdown guardado en: {ruta_guardado}")

vector_db, chunks = crear_pdf_store_vectore(documentos_cargados)

# 1. Definimos la pregunta del usuario
pregunta_usuario = "¿cómo se estructura el documento?"

# 2. Inicializamos el RAG
qa_chain = obtener_rag_chain(vector_db, chunks)

# 3. Ejecutamos el RAG principal
print("Generando respuesta inicial...")
resultado_rag = qa_chain.invoke({"query": pregunta_usuario})

# 4. Extraemos las dos piezas clave que necesita el juez
respuesta_generada = resultado_rag['result']
documentos_usados = resultado_rag['source_documents']

print(f"\nRespuesta generada por el agente:\n{respuesta_generada}\n")

# 5. Llamamos a tu función de auditoría con los datos correctos
print("Iniciando auditoría de calidad...")
verification_result = verificar_response_acuracy(
    retrieved_docs=documentos_usados, # Evidencia
    answer=respuesta_generada         # Respuesta (¡No la pregunta!)
)

print("\n=== Veredicto del Juez ===")
print(verification_result)
