from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""
    agente_actual = ""

    if request.method == "POST":

        agente_actual = request.form["agente"]
        consulta = request.form["consulta"]

        respuesta = f"""
        <h3>Resultado del agente: {agente_actual}</h3>
        <p>Consulta realizada:</p>
        <div style='background:#f1f2f6;padding:15px;border-radius:8px'>
        {consulta}
        </div>
        <br>
        <p>⚠️ Aquí luego aparecerá la respuesta generada por IA.</p>
        """

    return f"""
    <html>
    <head>
    <title>Sistema IA FUNCREDES</title>
    </head>

    <body style="margin:0;font-family:Arial">

    <div style="background:#0a3d62;color:white;padding:15px">
    <h2>Sistema Empresarial Multi-Agente IA</h2>
    </div>

    <div style="display:flex">

        <div style="width:260px;background:#dfe6e9;padding:20px;height:100vh">

        <h3>Agentes</h3>

        <p>🤖 Formulador Proyectos</p>
        <p>💰 Presupuestos</p>
        <p>📑 Licitaciones</p>
        <p>⚖️ Agente Legal</p>
        <p>📊 Evaluación Financiera</p>
        <p>📋 Diagnóstico</p>

        </div>

        <div style="flex:1;padding:40px">

        <h1>Panel de Consulta</h1>

        <form method="post">

        Seleccione agente:<br><br>

        <select name="agente" style="width:300px;height:35px">
        <option>Formulador Proyectos</option>
        <option>Presupuestos</option>
        <option>Licitaciones</option>
        <option>Agente Legal</option>
        <option>Evaluación Financiera</option>
        <option>Diagnóstico</option>
        </select>

        <br><br>

        Escriba la consulta:<br><br>

        <textarea name="consulta" style="width:500px;height:150px"></textarea>

        <br><br>

        <button style="padding:12px 25px;background:#0a3d62;color:white;border:0;border-radius:5px">
        Ejecutar Agente
        </button>

        </form>

        <br><br>

        {respuesta}

        </div>

    </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
