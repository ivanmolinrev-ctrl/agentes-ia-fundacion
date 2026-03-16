from flask import Flask, request, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

roles = {
"formulador":"Eres experto en formulación de proyectos en Colombia.",
"presupuestos":"Eres ingeniero civil experto en APU y costos.",
"licitaciones":"Eres experto en contratación estatal.",
"legal":"Eres abogado administrativo colombiano.",
"financiero":"Eres experto en evaluación financiera.",
"diagnostico":"Eres consultor organizacional."
}

# ================= PANEL =================

@app.route("/")
def panel():
    return render_template_string("""

<html>
<head>

<title>Sistema Multi-Agente IA</title>

<style>

body{
font-family:Arial;
background:#eef2f7;
margin:0;
}

.header{
background:#1e3c72;
color:white;
padding:20px;
text-align:center;
font-size:28px;
font-weight:bold;
}

.container{
padding:40px;
display:grid;
grid-template-columns:repeat(3,1fr);
gap:25px;
}

.card{
background:white;
padding:40px;
border-radius:15px;
box-shadow:0 5px 15px rgba(0,0,0,0.1);
text-align:center;
cursor:pointer;
transition:0.3s;
}

.card:hover{
transform:scale(1.05);
background:#f8f9ff;
}

a{
text-decoration:none;
color:black;
font-size:20px;
font-weight:bold;
}

</style>

</head>

<body>

<div class="header">
Dashboard Empresarial Multi-Agente IA
</div>

<div class="container">

<a href="/agente/formulador"><div class="card">🤖 Formulador Proyectos</div></a>
<a href="/agente/presupuestos"><div class="card">💰 Presupuestos Obra</div></a>
<a href="/agente/licitaciones"><div class="card">📑 Licitaciones</div></a>
<a href="/agente/legal"><div class="card">⚖️ Agente Legal</div></a>
<a href="/agente/financiero"><div class="card">📊 Evaluación Financiera</div></a>
<a href="/agente/diagnostico"><div class="card">📋 Diagnóstico Institucional</div></a>

</div>

</body>
</html>

""")

# ================= AGENTE =================

@app.route("/agente/<tipo>", methods=["GET","POST"])
def agente(tipo):

    respuesta = ""

    if request.method == "POST":

        consulta = request.form["consulta"]
        archivo = request.files.get("archivo")

        info_archivo = archivo.filename if archivo else ""

        prompt = roles[tipo] + f"""

Consulta:
{consulta}

Archivo adjunto:
{info_archivo}

Responder profesionalmente.
"""

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        respuesta = completion.choices[0].message.content

    return render_template_string("""

<html>
<head>

<style>

body{
font-family:Arial;
background:#eef2f7;
margin:0;
}

.topbar{
background:#1e3c72;
color:white;
padding:15px;
font-size:22px;
}

.box{
width:70%;
margin:auto;
margin-top:40px;
background:white;
padding:30px;
border-radius:15px;
box-shadow:0 5px 15px rgba(0,0,0,0.1);
}

textarea{
width:100%;
height:150px;
border-radius:10px;
padding:10px;
border:1px solid #ccc;
}

button{
background:#1e3c72;
color:white;
padding:12px 30px;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;
}

button:hover{
background:#16325c;
}

.resultado{
margin-top:30px;
background:#f4f6fb;
padding:20px;
border-radius:10px;
white-space:pre-wrap;
}

.volver{
display:inline-block;
margin-top:20px;
text-decoration:none;
font-weight:bold;
}

</style>

</head>

<body>

<div class="topbar">
Agente {{tipo}}
</div>

<div class="box">

<form method="post" enctype="multipart/form-data">

<textarea name="consulta" placeholder="Escribe tu consulta..."></textarea><br><br>

<input type="file" name="archivo"><br><br>

<button>Consultar IA</button>

</form>

<div class="resultado">
{{respuesta}}
</div>

<a class="volver" href="/">⬅ Volver al panel</a>

</div>

</body>
</html>

""", tipo=tipo.upper(), respuesta=respuesta)

if __name__ == "__main__":
    app.run()
