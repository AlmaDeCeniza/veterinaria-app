import os
import requests
from dotenv import load_dotenv

# ===================================================
# CONFIGURACIÓN GENERAL
# ===================================================

load_dotenv()
API_KEY = ''
#API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "deepseek/deepseek-chat"

# ===================================================
# FUNCIÓN CENTRAL IA
# ===================================================

def generar_respuesta_ia(prompt):

    if not API_KEY:
        return """
        <div class='bg-red-500/10 border border-red-500/20
        text-red-300 p-5 rounded-2xl'>

            No se encontró la API KEY de OpenRouter.

        </div>
        """

    try:

        response = requests.post(
            url=BASE_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Veterinaria Inteligente"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": """
                        Eres un experto en veterinaria, análisis de datos, inteligencia empresarial y gestión clínica.

                        REGLAS CRÍTICAS DE RESPUESTA:
                        1. Responde ÚNICAMENTE con fragmentos de HTML (div, h2, p, ul, li, span).
                        2. NUNCA incluyas etiquetas <html>, <head>, <body> o <!DOCTYPE>.
                        3. NO uses bloques de código markdown (no uses ```html).
                        4. NO escribas introducciones como "Aquí tienes el análisis" o "Claro, aquí está".
                        5. Asegúrate de que todas las etiquetas <div> estén correctamente cerradas.
                        6. Usa clases de Tailwind CSS si es necesario para mejorar la estética, pero mantente dentro de la estructura de fragmentos.
                        """
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 900
            },
            timeout=25
        )

        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # 1. Limpiar bloques de código Markdown (ej: ```html ... ```)
        if "```" in content:
            import re
            match = re.search(r"```(?:html)?\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1)

        # 2. Sanitización de etiquetas raíz (Evitar que la IA envíe <html> o <body>)
        import re
        content = re.sub(r'<(html|body|head|meta)[^>]*>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'</(html|body|head|meta)>', '', content, flags=re.IGNORECASE)

        return content

    except Exception as e:

        return f"""
        <div class='bg-red-500/10 border border-red-500/20
        text-red-300 p-5 rounded-2xl'>

            Error IA: {str(e)}

        </div>
        """


# ===================================================
# CONSULTAS POR VETERINARIO
# ===================================================

def consultas_por_veterinario(data):

    veterinarios_str = "\n".join([
        f"- {nombre}: {consultas} consultas"
        for nombre, consultas in data
    ])

    prompt = f"""
    Analiza esta lista de veterinarios:

    {veterinarios_str}

    Genera un análisis profesional HTML.

    ESTRUCTURA:

    <h2>Análisis General</h2>

    <h2>Veterinarios Más Destacados</h2>

    <h2>Posibles Sobrecargas</h2>

    <h2>Recomendaciones de Gestión</h2>

    <h2>Conclusión</h2>

    REGLAS:
    - Solo HTML
    - No markdown
    - Diseño elegante
    - Usa ul y li
    - Usa párrafos cortos
    """

    return generar_respuesta_ia(prompt)


# ===================================================
# ANALIZAR RECURRENCIA
# ===================================================

def analizar_recurrencia(data):

    pacientes_str = "\n".join([
        f"- {nombre} ({especie}): {visitas} visitas"
        for nombre, especie, visitas in data
    ])

    prompt = f"""
    Analiza estos pacientes recurrentes:

    {pacientes_str}

    Genera un informe veterinario profesional.

    ESTRUCTURA:

    <h2>Resumen Clínico</h2>

    <h2>Pacientes Crónicos</h2>

    <h2>Riesgos Potenciales</h2>

    <h2>Recomendaciones Preventivas</h2>

    <h2>Consejo Administrativo</h2>

    REGLAS:
    - Solo HTML
    - No markdown
    - Usa listas
    - Usa párrafos modernos
    """

    return generar_respuesta_ia(prompt)


# ===================================================
# ANALIZAR TENDENCIAS
# ===================================================

def analizar_tendencias(data):

    tendencias_str = "\n".join([
        f"- {mes}: {cantidad} consultas"
        for mes, cantidad in data
    ])

    prompt = f"""
    Analiza estas tendencias veterinarias:

    {tendencias_str}

    Genera un análisis ejecutivo HTML.

    ESTRUCTURA:

    <h2>Comportamiento General</h2>

    <h2>Meses con Mayor Actividad</h2>

    <h2>Posibles Causas</h2>

    <h2>Estrategias Recomendadas</h2>

    <h2>Conclusión Ejecutiva</h2>

    REGLAS:
    - Solo HTML
    - No markdown
    - Usa listas y párrafos
    """

    return generar_respuesta_ia(prompt)


# ===================================================
# CONSULTAS POR ESPECIE
# ===================================================

def consultas_por_especie(data):

    especies_str = "\n".join([
        f"- {especie}: {consultas} consultas"
        for especie, consultas in data
    ])

    prompt = f"""
    Analiza las siguientes consultas por especie:

    {especies_str}

    Genera un informe veterinario profesional HTML.

    ESTRUCTURA:

    <h2>Análisis por Especies</h2>

    <h2>Especies Más Atendidas</h2>

    <h2>Posibles Enfermedades Frecuentes</h2>

    <h2>Recomendaciones Clínicas</h2>

    <h2>Conclusión</h2>

    REGLAS:
    - Solo HTML
    - Diseño elegante
    - Usa listas
    - No markdown
    """

    return generar_respuesta_ia(prompt)


# ===================================================
# ANALIZAR PACIENTES
# ===================================================

def analizar_pacientes(data):

    pacientes_str = "\n".join([
        f"- {nombre} | {especie} | {edad} años"
        for nombre, especie, edad in data
    ])

    prompt = f"""
    Analiza esta lista de pacientes:

    {pacientes_str}

    Genera un informe veterinario inteligente.

    ESTRUCTURA:

    <h2>Resumen General</h2>

    <h2>Distribución de Pacientes</h2>

    <h2>Factores de Riesgo</h2>

    <h2>Sugerencias Preventivas</h2>

    <h2>Conclusión Clínica</h2>

    REGLAS:
    - Solo HTML
    - No markdown
    - Usa listas y párrafos
    """

    return generar_respuesta_ia(prompt)