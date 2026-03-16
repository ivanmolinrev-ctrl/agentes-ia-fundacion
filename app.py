from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""

    if request.method == "POST":
        idea = request.form["idea"]

        respuesta = f"""
        PROYECTO GENERADO

        Idea: {idea}

        Objetivo:
        Desarrollar un proyecto basado en la idea propuesta.

        Beneficiarios:
        Comunidad local.

        Presupuesto estimado:
        $500.000.000

        Duración:
        6 meses
        """

    return f"""
    <h1>Agente IA Formulador de Proyectos</h1>

    <form method="post">
    Escribe la idea del proyecto:<br><br>
    <input name="idea" style="width:300px">
    <br><br>
    <button>Generar Proyecto</button>
    </form>

    <pre>{respuesta}</pre>
    """

if __name__ == "__main__":
    app.run()
