from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

roles = {

"Formulador":
"""
Eres un experto en formulación de proyectos públicos y privados en Colombia.
Especialista en MGA, PMI, estudios técnicos, financieros y sociales.
Redactas proyectos completos con estructura profesional.
""",

"Presupuestos":
"""
Eres ingeniero civil experto en presupuestos de obra.
Realizas APU, AIU, cronogramas, análisis de costos y control financiero.
Utilizas criterios reales del mercado colombiano.
""",

"Licitaciones":
"""
Eres experto en contratación estatal colombiana.
Analizas pliegos, requisitos habilitantes, factores de evaluación y estrategias.
""",

"Legal":
"""
Eres abogado experto en derecho administrativo colombiano.
Redactas derechos de petición, respuestas a entidades, recursos y conceptos jurídicos.
""",

"Financiero":
"""
Eres experto en evaluación financiera de proyectos.
Realizas VAN, TIR, flujo de caja, análisis de riesgo y sostenibilidad.
""",

"Diagnostico":
"""
Eres consultor organizacional experto en fortalecimiento institucional.
Analizas procesos, talento humano, estructura y sostenibilidad.
"""
}

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""
    agente = ""
    consulta = ""

    if request.method == "POST":

        agente = request.form["agente"]
        consulta = request.form["consulta"]

        prompt = roles[agente] + f"""

Consulta del usuario:
{consulta}

Responde de forma técnica, clara, estructurada y profesional.
"""

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        respuesta = completion.choices[0].message.content

    return f"""
<html>
<head>
<title>Sistema IA FUNCREDES</title>
</head>

<body style="margin:0;font-family:Arial;background:#f5f6fa">

<div style="background:#0a3d62;color:white;padding:20px">
<h2>Dashboard Empresarial Multi-Agente IA</h2>
</div>

<div style="display:flex">

<div style="width:260px;background:white;padding:20px;height:100vh;box-shadow:2px 0 5px rgba(0,0,0,0.1)">

<h3>Agentes IA</h3>

<form method="post">

<button name="agente" value="Formulador" style="width:100%;padding:15px;margin-bottom:10px;background:#27ae60;color:white;border:0;border-radius:8px;font-size:16px">🤖 Formulador Proyectos</button>

<button name="agente" value="Presupuestos" style="width:100%;padding:15px;margin-bottom:10px;background:#e67e22;color:white;border:0;border-radius:8px;font-size:16px">💰 Presupuestos</button>

<button name="agente" value="Licitaciones" style="width:100%;padding:15px;margin-bottom:10px;background:#2980b9;color:white;border:0;border-radius:8px;font-size:16px">📑 Licitaciones</button>

<button name="agente" value="Legal" style="width:100%;padding:15px;margin-bottom:10px;background:#8e44ad;color:white;border:0;border-radius:8px;font-size:16px">⚖️ Agente Legal</button>

<button name="agente" value="Financiero" style="width:100%;padding:15px;margin-bottom:10px;background:#c0392b;color:white;border:0;border-radius:8px;font-size:16px">📊 Evaluación Financiera</button>

<button name="agente" value="Diagnostico" style="width:100%;padding:15px;margin-bottom:10px;background:#16a085;color:white;border:0;border-radius:8px;font-size:16px">📋 Diagnóstico</button>

<br><br>

<textarea name="consulta" placeholder="Escribe tu consulta..." style="width:100%;height:120px;border-radius:8px;padding:10px"></textarea>

</form>

</div>

<div style="flex:1;padding:40px">

<h1>Resultado del Agente</h1>

<div style="background:white;padding:30px;border-radius:10px;box-shadow:0 0 10px rgba(0,0,0,0.1)">
{respuesta}
</div>

</div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run()
