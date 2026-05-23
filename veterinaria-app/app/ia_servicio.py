import requests
import json
# creen y añadan su KEY

#API_KEY = '' #add KEY
API_KEY = '' 

def consultas_por_veterinario(data):
    """
    Analiza las consultas por veterinario y genera recomendaciones.
    data: Lista de tuplas (nombre_veterinario, conteo_consultas)
    """
    # Formatear los datos para la IA
    veterinarios_str = "\n".join([f"- {nombre}: {consultas} consultas" for nombre, consultas in data])

    prompt = f"""
        Actúa como un experto en gestión de clínicas veterinarias.
        Analiza la siguiente lista de veterinarios con mayor número de consultas:

        {veterinarios_str}

        Genera un informe breve en formato HTML (usa solo etiquetas básicas como <ul>, <li>, <strong>, <p> y <br>).
        No incluyas etiquetas <html>, <head> o <body>.

        El informe debe seguir estrictamente esta estructura:
        1. <strong>Análisis de Consultas</strong> Un breve comentario sobre lo que significan estas cifras para la clínica.
        2. <strong>Sugerencias para el Equipo</strong> Identifica posibles áreas de mejora o capacitación para los veterinarios con más consultas.
        3. <strong>Consejo de Gestión</strong> Una sugerencia para optimizar la distribución de consultas entre el equipo.
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"<p>Lo sentimos, no se pudo generar el análisis de la IA en este momento. (Error: {str(e)})</p>"


def analizar_recurrencia(data):
    """
    Analiza la recurrencia de pacientes y genera recomendaciones veterinarias.
    data: Lista de tuplas (nombre, especie, conteo)
    """
    # Formatear los datos para la IA
    pacientes_str = "\n".join([f"- {nombre} ({especie}): {visitas} visitas" for nombre, especie, visitas in data])

    prompt = f"""
        Actúa como un experto en medicina veterinaria y gestión de clínicas.
        Analiza la siguiente lista de pacientes con mayor recurrencia de visitas:

        {pacientes_str}

        Genera un informe breve en formato HTML (usa solo etiquetas básicas como <ul>, <li>, <strong>, <p> y <br>).
        No incluyas etiquetas <html>, <head> o <body>.

        IMPORTANTE: No pongas dos puntos (:) ni ningún signo de puntuación inmediatamente después de cerrar la etiqueta </strong>.

        El informe debe seguir estrictamente esta estructura:
        1. <strong>Análisis de Recurrencia</strong> Un breve comentario sobre lo que significan la cifra de visitas para la clínica.
        2. <strong>Sugerencias Clínicas</strong> Identifica patrones (ej. pacientes que podrían tener enfermedades crónicas) y sugiere qué pruebas o seguimientos preventivos se podrían recomendar.
        3. <strong>Consejo de Gestión</strong> Una sugerencia para mejorar la atención de estos pacientes recurrentes.
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"<p>Lo sentimos, no se pudo generar el análisis de la IA en este momento. (Error: {str(e)})</p>"
