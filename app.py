import streamlit as st
import requests

# URL del Space Gradio como backend
API_URL = "https://cdega-analista3.hf.space/api/predict/"

# Configuración de la app
st.set_page_config(page_title="Asistente de Análisis de Software", page_icon="🤖")
st.title("🤖 Asistente de Análisis de Software")

# Inputs del usuario
apps = st.text_input("📱 Nombre(s) de la(s) aplicación(es):", placeholder="Ej: Replika, Notion")
contexto = st.text_input("🎯 ¿Algún contexto o uso específico?", placeholder="Ej: enseñanza de idiomas, productividad")
tipo = st.radio("🔎 Tipo de análisis", ["Breve", "Completo"])

# Botón de análisis
if st.button("Analizar"):
    if not apps and not contexto:
        st.warning("Por favor, introduce al menos una aplicación o un contexto.")
    else:
        # Construir prompt
        if apps:
            prompt = f"""
Actúa como un asistente en castellano experto en análisis de software. 
Usuario ha indicado las siguientes apps: {apps}
Contexto específico: {contexto if contexto else 'Ninguno'}
Desea un análisis tipo: {tipo}

🔁 Instrucciones generales:
- Si el usuario proporciona una sola app, analiza según la estructura detallada.
- Si da varias apps separadas por comas, compáralas al final.
- Adapta el análisis al contexto dado.
- Estructura del análisis:
1. Nombre y categoría
2. Resumen general
3. Instalación y configuración
4. Puntos fuertes
5. Puntos débiles
6. Impacto en la sociedad
7. Sugerencias de mejora
8. Alternativas y comparativa
9. ¿Recomendada?
"""
        else:
            prompt = f"""
Actúa como un asistente en castellano experto en análisis de software.
El usuario no ha especificado ninguna aplicación, pero sí un contexto de uso: "{contexto}".
Tu tarea es recomendarle las mejores aplicaciones disponibles actualmente para ese caso,
explicando brevemente qué hace cada una, sus ventajas y en qué situaciones se destaca.
Al final, sugiere cuál es la mejor opción según lo descrito.

Estructura sugerida:
1. Recomendaciones principales (nombre y descripción breve)
2. Comparativa de ventajas
3. Recomendación final con justificación
"""

        # Enviar al backend Gradio
        with st.spinner("Consultando modelo en el backend..."):
            try:
                response = requests.post(API_URL, json={"data": [prompt]}, timeout=45)
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["data"][0])
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Error al conectar con el backend: {e}")
