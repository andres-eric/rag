import os
import re
import shutil
import warnings
import logging
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.ERROR)
import streamlit as st
import pymupdf4llm
from dotenv import find_dotenv, load_dotenv
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_cohere import CohereEmbeddings
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_cohere import CohereRerank
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Importaciones necesarias para la arquitectura LCEL
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
#from langchain.output_parsers import JsonOutputParser
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import time
from langchain_core.runnables import RunnableLambda
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Annoy
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from ddgs import DDGS
from langchain.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.ddg_search.tool import DDGInput
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langgraph.prebuilt import ToolNode

load_dotenv(find_dotenv())




@tool
def google_search(query:str)->str:
    """Busca en internet usando DuckDuckGo Search y devuelve los resultados.
    Útil cuando necesitas buscar información actualizada, noticias o datos recientes."""
    try: 
        resultados=DDGS().text(query, max_results=4)
        texto_limpio="\n".join(f"Link de la noticia: {res['href']}\nNoticia: {res['body']}"   for res in resultados )
        #print(texto_limpio)
        return texto_limpio
    except Exception as e:
        return f"Error al buscar en Google: {e}"

@tool
def caculadora_de_raices(numero:float)->float:
    """Calcula la raíz cuadrada de un número."""

    raiz=numero**0.5
    if raiz>0:
        return raiz
    else:
        raise ValueError("El número complejo no se puede calcular")

    

def tool_llm():
    try:
        llm_gemini_instance = ChatOllama(
            model="llama3.1",
            base_url="http://localhost:11434",  # URL por defecto de Ollama
            temperature=0.0, 
        )
        print("Modelo llama3.1 (Ollama local) inicializado correctamente.")
        return llm_gemini_instance
    except Exception as e:
        print(f"ERROR: Falló la inicialización de ChatOllama. Asegúrate de que Ollama esté corriendo. Mensaje: {e}")
        return None


def busqueda(pregunta):

        herramientas= [caculadora_de_raices,google_search]


        mapear_herramientas={
            i.name:i for i in herramientas
        }
        


        #"atar" o "vincular" temporalmente la información de tus
        # herramientas al modelo y devolver un objeto nuevo modificado que guardas en la variable ll_herramientas.
        #la variable ll_herramientas ahora guarda ese modelo modificado.
        ll_herramientas=tool_llm().bind_tools(herramientas)



        prompt_especializado = SystemMessage(content="""
        Eres un Analista Comercial Senior de Licitaciones B2B para una empresa líder en energía renovable y transición energética.
        Acabas de recibir resultados crudos de extracción web sobre licitaciones de paneles solares y sistemas fotovoltaicos.

        TU MISIÓN:
        Filtrar el ruido de internet e identificar ÚNICAMENTE oportunidades de negocio reales, accionables y vigentes para la empresa.

        CRITERIOS DE BÚSQUEDA Y CALIFICACIÓN (REGLAS ESTRICTAS):
        1. GEOGRAFÍA Y JURISDICCIÓN: Solo licitaciones, invitaciones o proyectos dentro del territorio de Colombia (Entidades nacionales, departamentales o alcaldías).
        2. ESTADO DEL PROCESO (VIGENCIA): Busca únicamente procesos "Abiertos", "En Borrador", "Convocatoria pública" o "Próximos a abrir". IGNORA por completo contratos "Adjudicados", "Terminados", "Liquidados" o noticias de años anteriores.
        3. ALCANCE B2B (TAMAÑO): Prioriza compras corporativas/estatales (Suministro masivo, Instalación EPC, Granjas Solares, Alumbrado Público Solar, Techos Industriales). IGNORA compras residenciales (B2C) o menudeo.
        4. EXCLUSIONES DE RUIDO: Descarta noticias puramente periodísticas de inauguraciones, artículos de opinión, y si el texto es código basura (HTML/JavaScript), sáltalo.

        FORMATO DE RESPUESTA ESTRICTO:
        Para cada oportunidad que supere TODOS los filtros anteriores, redacta el hallazgo usando exactamente esta estructura. Si no encuentras ninguna válida, responde: "No se encontraron licitaciones vigentes que cumplan con los criterios B2B en esta búsqueda."

        🔸 ENTIDAD: [Nombre oficial de la entidad pública o empresa privada]
        🔸 DESCRIPCIÓN TÉCNICA: [Resumen conciso de 2 líneas sobre el alcance del proyecto o lo que se va a comprar]
        🔸 ESTADO INFERIDO: [Ej: Probablemente Abierta / En planeación / Convocatoria]
        🔸 EVALUACIÓN COMERCIAL: [Justificación estratégica de por qué este proyecto hace 'match' con nuestro negocio B2B]
        🔸 LINK: https://datos.gob.es/es/blog/datos-no-tradicionales-que-son-y-por-que-cada-vez-se-usan-mas
        """)

            
        mensajes = [
            SystemMessage(content="Eres un asistente útil con acceso a herramientas."),
            HumanMessage(content=pregunta)
        ]



        #El método invoke sí tiene parámetros: está diseñado para recibir una lista de mensajes (mensajes) 
        #y enviarlos a la API del modelo (en tu caso, Ollama ejecutándose localmente).
        respuesta=ll_herramientas.invoke(mensajes)

        if respuesta.tool_calls:
            

            #Esta línea es crucial: le dice al modelo "Aquí tienes la respuesta inicial que acabo de recibir de una de tus 
            # herramientas. Úsala para continuar tu razonamiento."
            mensajes.append(respuesta)

            for i in respuesta.tool_calls:
                nombre=i['name']

                
                if nombre in mapear_herramientas:
                    herramienta=mapear_herramientas[nombre]
                    resultado=herramienta.invoke(i['args'])
                    mensajes.append(ToolMessage(content=str(resultado), tool_call_id=i['id']))
            
            respuesta_final=ll_herramientas.invoke(mensajes)
            print(respuesta_final.content)
        else:
            print(respuesta.content)



pregunta="¿Cuál es la raíz cuadrada de 1681 y traeme licitaciones que tenga el estado colombiano o contrataciones acerca de paneles solares?"

busqueda(pregunta)






