import sys, subprocess
try:
    import langchain_experimental
except ImportError:
    print("Instalando langchain-experimental automáticamente en tu entorno activo...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-experimental", "langchain-community", "langchain-core", "langchain-text-splitters"])

# =============================================================================
# INSTRUCCIONES DE EJECUCIÓN — LEER ANTES DE CORRER
# =============================================================================
#
# 1. VERIFICAR QUE OLLAMA ESTÉ CORRIENDO (servidor local de IA):
#    Ollama normalmente arranca automático con Windows. Para verificarlo:
#
#    PowerShell:
#       & "C:\Users\afonseca\AppData\Local\Programs\Ollama\ollama.exe" ps
#
#    Si no hay modelos activos, Ollama igual está corriendo en background.
#    Si aparece error de "puerto en uso" al intentar iniciarlo = ya está activo ✅
#
#    Para iniciarlo manualmente (solo si no está corriendo):
#       & "C:\Users\afonseca\AppData\Local\Programs\Ollama\ollama.exe" serve
#
# 2. MODELO USADO: deepseek-r1:1.5b (corre en GPU NVIDIA RTX PRO 2000 Blackwell)
#    Para verificar que el modelo está instalado:
#       & "C:\Users\afonseca\AppData\Local\Programs\Ollama\ollama.exe" list
#
#    Para instalarlo si no está:
#       & "C:\Users\afonseca\AppData\Local\Programs\Ollama\ollama.exe" pull deepseek-r1:1.5b
#
# 3. VERIFICAR USO DE GPU (CUDA):
#    PowerShell:
#       nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader
#    Si memory.used sube cuando corre el modelo = está usando GPU 
#
# 4. EJECUTAR ESTE SCRIPT:
#    PowerShell:
#       & "\\belenus\IT\ComandosSQL\sql scripts-Esteban\LL R\chat bot-12\BM25\.venv\Scripts\python.exe" `
#         "\\belenus\IT\ComandosSQL\sql scripts-Esteban\LL R\chat bot-12\Ollama\RE rank\main.py"
#
# 5. NOTAS IMPORTANTES:
#    - ChromaDB se guarda LOCAL en: C:\Users\afonseca\chroma_db  (NO en la red)
#    - El PDF fuente está en: \\belenus\...\chat bot-12\ti.pdf
#    - Los archivos están en red (\\belenus) pero la IA corre en tu PC local
# =============================================================================

import os
import logging
from dotenv import find_dotenv, load_dotenv
from utils import limpiar_markdown, guardar_markdown
from agente import crear_pdf_store_vectore, obtener_rag_chain,definir_pregunt
import time

#logging.getLogger("streamlit").setLevel(logging.ERROR)
load_dotenv(find_dotenv())

# Obtener la ruta base del proyecto (raíz de chat bot-12, 3 niveles arriba de main.py)
# main.py está en: chat bot-12/Ollama/RE rank/main.py
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

pregunta_original="¿Cuáles son las dos máquinas virtuales que actúan en el esquema de réplica del servidor TARANIS, pero que tienen una directriz específica que prohíbe realizar sus backups en el transcurso del día normal? "


print(f"pregunta original : {pregunta_original}")
pregunta_expandida = definir_pregunt(pregunta_original)

inicio = time.perf_counter()
vector_db, chunks = crear_pdf_store_vectore(documentos_cargados)
fin = time.perf_counter()



#print(f"Tiempo transcurrido: {fin - inicio}")
qa_chain = obtener_rag_chain(vector_db, chunks,pregunta_expandida)
minutos_llm=int(fin - inicio)//60
segundos_llm=round((fin - inicio)%60,2)
print(f"⏱️ Tiempo total: {minutos_llm}m {segundos_llm:.2f}s ({fin - inicio} segundos)")
fin_programa = time.perf_counter()
minutos_programa=int(fin_programa-tiempo_inicio_programa)//60
segundos_programa=round((fin_programa-tiempo_inicio_programa)%60,2)
print(f"⏱️ Tiempo total del programa: {minutos_programa}m {segundos_programa:.2f}s ({fin_programa-tiempo_inicio_programa} segundos)")

