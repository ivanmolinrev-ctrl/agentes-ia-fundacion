from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""

    if request.method == "POST":

        agente = request.form["agente"]
        consulta = request.form["consulta"]

        prompt = f"""
        Actúa como un experto profesional en el área:
        {agente}

        Responde de manera técnica, clara y estructurada:

        Consulta:
        {consulta}
        """

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        respuesta = completion.choices[0].message.content

    return f"""
    <html>
    <body style="font-family:Arial">

    <h1>Sistema Multi-Agente IA FUNCREDES</h1>

    <form method="post">

    Seleccione agente:<br><br>

    <select name="agente">
    <option>Formulador de Proyectos</option>
    <option>Ingeniero de Presupuestos</option>
    <option>Buscador de Licitaciones</option>
    <option>Abogado Institucional</option>
    <option>Evaluador Financiero</option>
    <option>Consultor Organizacional</option>
    </select>

    <br><br>

    Consulta:<br><br>

    <textarea name="consulta" style="width:500px;height:150px"></textarea>

    <br><br>

    <button>Consultar IA</button>

    </form>

    <br><br>

    <div style="background:#f1f2f6;padding:20px;border-radius:10px">
    {respuesta}
    </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
