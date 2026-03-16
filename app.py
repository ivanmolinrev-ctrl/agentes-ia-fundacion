from flask import Flask, request, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

roles = {

"formulador":
"""
Eres experto en formulación de proyectos en Colombia.
Especialista MGA, PMI, estudios técnicos, sociales y financieros.
""",

"presupuestos":
"""
Eres ingeniero civil experto en APU, AIU, cronogramas y costos reales.
""",

"licitaciones":
"""
Eres experto en contratación estatal colombiana y SECOP.
""",

"legal":
"""
Eres abogado experto en derecho administrativo colombiano.
Redactas derechos de petición, tutelas y respuestas institucionales.
""",

"financiero":
"""
Eres experto en VAN, TIR, flujo de caja y evaluación de proyectos.
""",

"diagnostico":
"""
Eres consultor en fortalecimiento organizacional e institucional.
"""
}

# ================= PANEL PRINCIPAL =================

@app.route("/")
def panel():

    return """
    <h1>Dashboard Multi-Agente IA</h1>

    <a href='/agente/formulador'><button>🤖 Formulador</button></a>
    <a href='/agente/presupuestos'><button>💰 Presupuestos</button></a>
    <a href='/agente/licitaciones'><button>📑 Licitaciones</button></a>
    <a href='/agente/legal'><button>⚖️ Legal</button></a>
    <a href='/agente/financiero'><button>📊 Financiero</button></a>
    <a href='/agente/diagnostico'><button>📋 Diagnóstico</button></a>
    """

# ================= PANTALLA DE CADA AGENTE =================

@app.route("/agente/<tipo>", methods=["GET","POST"])
def agente(tipo):

    respuesta = ""

    if request.method == "POST":

        consulta = request.form["consulta"]

        archivo = request.files.get("archivo")

        texto_archivo = ""

        if archivo:
            texto_archivo = f"El usuario adjuntó archivo llamado {archivo.filename}"

        prompt = roles[tipo] + f"""

Consulta:
{consulta}

Información archivo:
{texto_archivo}

Responder profesionalmente.
"""

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        respuesta = completion.choices[0].message.content

    return render_template_string(f"""

    <h2>Agente {tipo.upper()}</h2>

    <form method="post" enctype="multipart/form-data">

    <textarea name="consulta" style="width:400px;height:120px"></textarea><br><br>

    Adjuntar archivo:<br>
    <input type="file" name="archivo"><br><br>

    <button>Enviar a IA</button>

    </form>

    <hr>

    <div>{respuesta}</div>

    <br><br>
    <a href="/">Volver al panel</a>

    """)

if __name__ == "__main__":
    app.run()
