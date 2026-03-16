from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    respuesta = ""

    if request.method == "POST":

        agente = request.form["agente"]
        consulta = request.form["consulta"]

        if agente == "legal":

            respuesta = f"""
            <h3>Respuesta Jurídica Generada</h3>

            Consulta:
            {consulta}

            Concepto:

            En atención a su solicitud, se procede a emitir respuesta
            institucional indicando que la entidad ha actuado conforme
            a la normatividad vigente y principios de la función pública.

            Se recomienda adjuntar soportes documentales y
            mantener comunicación con la entidad requirente.
            """

        if agente == "proyectos":

            respuesta = f"""
            <h3>Proyecto Generado</h3>

            Idea:
            {consulta}

            Objetivo:
            Desarrollar un proyecto social sostenible.

            Beneficiarios:
            Población vulnerable.

            Presupuesto:
            $600.000.000

            Duración:
            7 meses
            """

    return f"""
    <html>
    <body style="font-family:Arial">

    <h1>Sistema Empresarial de Agentes IA</h1>

    <form method="post">

    Seleccione Agente:<br><br>

    <select name="agente">
    <option value="proyectos">Agente Formulador</option>
    <option value="legal">Agente Legal</option>
    </select>

    <br><br>

    Escriba la consulta:<br><br>

    <textarea name="consulta" style="width:400px;height:120px"></textarea>

    <br><br>

    <button>Generar</button>

    </form>

    <br><br>

    {respuesta}

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
