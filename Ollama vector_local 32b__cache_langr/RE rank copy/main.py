import os
import time
import logging
from dotenv import find_dotenv, load_dotenv
from utils import limpiar_markdown, guardar_markdown
from agente import crear_pdf_store_vectore, definir_pregunt, obtener_rag_chain


logging.basicConfig(level=logging.ERROR)
load_dotenv(find_dotenv())

def main():
    print(" INICIANDO SISTEMA RAG CON LANGGRAPH...\n")
    tiempo_inicio_programa = time.perf_counter()

  
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.join(base_dir, "ti.pdf")
    
    print(f"📄 Procesando documento: {full_path}")
    documentos_cargados = limpiar_markdown(full_path)

    
    texto_completo = "\n\n".join([doc.page_content for doc in documentos_cargados])
    ruta_guardado = os.path.join(os.path.dirname(full_path), "documento_salida.md")
    guardar_markdown(texto_completo, ruta_guardado)
    print(f"✅ Markdown guardado en: {ruta_guardado}\n")

    # =========================================================
    # 2. CREACIÓN DE BASE VECTORIAL (ChromaDB + Caché)
    # =========================================================
    print("⏳ Creando base de datos vectorial...")
    inicio_db = time.perf_counter()
    
    vector_db, chunks = crear_pdf_store_vectore(documentos_cargados)
    
    fin_db = time.perf_counter()
    print(f"✅ Base de datos lista en {round(fin_db - inicio_db, 2)} segundos.\n")

    # =========================================================
    # 3. DEFINIR PREGUNTA Y EJECUTAR AGENTE LANGGRAPH
    # =========================================================
    pregunta_original = "Existe un procedimiento de copias adicionales de disco que no están diseñadas para restaurarse, sino para reemplazar directamente un disco virtual afectado. ¿En qué unidad de almacenamiento (NAS) específica se guardan estas copias diarias y por qué SARASVATI tiene un trato excepcional en el número de copias retenidas? "
    
    print("=" * 60)
    print(f"👤 PREGUNTA ORIGINAL:\n{pregunta_original}")
    print("=" * 60)

    # Expandir pregunta
    pregunta_expandida = definir_pregunt(pregunta_original)

    print("\n🤖 El Agente está investigando el caso...")
    inicio_llm = time.perf_counter()
    
    # Invocamos la cadena que contiene tu Grafo compilado
    respuesta_final = obtener_rag_chain(vector_db, chunks, pregunta_expandida)
    
    fin_llm = time.perf_counter()

    # =========================================================
    # 4. RESULTADOS Y MÉTRICAS
    # =========================================================
    print("\n" + "=" * 60)
    print("🏆 RESULTADO FINAL DEL AUDITOR FORENSE")
    print("=" * 60)
    print(respuesta_final)
    print("=" * 60)

    # Cálculo de tiempos
    minutos_llm = int(fin_llm - inicio_llm) // 60
    segundos_llm = round((fin_llm - inicio_llm) % 60, 2)
    print(f"\n⏱️ Tiempo del modelo LLM (LangGraph): {minutos_llm}m {segundos_llm}s ({round(fin_llm - inicio_llm, 2)} segundos)")
    
    fin_programa = time.perf_counter()
    minutos_programa = int(fin_programa - tiempo_inicio_programa) // 60
    segundos_programa = round((fin_programa - tiempo_inicio_programa) % 60, 2)
    print(f"⏱️ Tiempo total del script: {minutos_programa}m {segundos_programa}s ({round(fin_programa - tiempo_inicio_programa, 2)} segundos)")

# Punto de entrada estándar en Python
if __name__ == "__main__":
    main()