from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""

    if request.method == "POST":
        idea = request.form["idea"]

        respuesta = f"""
        <h3>Proyecto generado</h3>
        Idea: {idea} <br><br>

        Objetivo:
        Desarrollar un proyecto social basado en la idea propuesta.

        Beneficiarios:
        Comunidad vulnerable.

        Presupuesto:
        $800.000.000

        Duración:
        8 meses
        """

    return f"""
    <html>
    <head>
    <title>Sistema IA Fundación</title>
    </head>

    <body style="font-family: Arial; margin:0">

    <div style="background:#0a3d62;color:white;padding:15px">
    <h2>Sistema Empresarial de Agentes IA</h2>
    </div>

    <div style="display:flex">

        <div style="width:250px;background:#dfe6e9;padding:20px;height:100vh">
        <h3>Menú</h3>
        <p>Formulador</p>
        <p>Presupuestos</p>
        <p>Licitaciones</p>
        <p>Diagnóstico</p>
        </div>

        <div style="flex:1;padding:40px">

        <h1>Agente IA Formulador</h1>

        <form method="post">
        Idea del proyecto:<br><br>
        <input name="idea" style="width:400px;height:35px">
        <br><br>
        <button style="padding:10px 20px;background:#0a3d62;color:white;border:0">
        Generar Proyecto
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
