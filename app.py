from flask import Flask, request, render_template_string
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

roles = {
"formulador":"Eres experto en formulación de proyectos.",
"presupuestos":"Eres ingeniero experto en presupuestos.",
"licitaciones":"Eres experto en contratación estatal.",
"legal":"Eres abogado administrativo.",
"financiero":"Eres experto financiero.",
"diagnostico":"Eres consultor organizacional."
}

# ================= DASHBOARD =================

@app.route("/")
def panel():
    return render_template_string("""

<html>
<head>
<title>Plataforma IA FUNCREDES</title>

<style>

body{
margin:0;
font-family:Arial;
background:#f1f4f9;
}

.sidebar{
position:fixed;
width:240px;
height:100%;
background:#0b2545;
color:white;
padding:20px;
}

.logo{
font-size:22px;
font-weight:bold;
margin-bottom:30px;
}

.menu a{
display:block;
color:white;
text-decoration:none;
padding:12px;
border-radius:8px;
margin-bottom:10px;
transition:0.3s;
}

.menu a:hover{
background:#133c73;
}

.content{
margin-left:260px;
padding:40px;
}

.cards{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:25px;
}

.card{
background:white;
padding:30px;
border-radius:15px;
box-shadow:0 6px 18px rgba(0,0,0,0.1);
font-size:18px;
font-weight:bold;
cursor:pointer;
transition:0.3s;
text-align:center;
}

.card:hover{
transform:translateY(-5px);
}

</style>

</head>

<body>

<div class="sidebar">

<div class="logo">FUNCREDES IA</div>

<div class="menu">
<a href="/">🏠 Inicio</a>
<a href="/agente/formulador">🤖 Formulador</a>
<a href="/agente/presupuestos">💰 Presupuestos</a>
<a href="/agente/licitaciones">📑 Licitaciones</a>
<a href="/agente/legal">⚖️ Legal</a>
<a href="/agente/financiero">📊 Financiero</a>
<a href="/agente/diagnostico">📋 Diagnóstico</a>
</div>

</div>

<div class="content">

<h1>Panel de Agentes Inteligentes</h1>

<div class="cards">

<a href="/agente/formulador"><div class="card">🤖 Formular Proyecto</div></a>
<a href="/agente/presupuestos"><div class="card">💰 Presupuesto Obra</div></a>
<a href="/agente/licitaciones"><div class="card">📑 Analizar Licitación</div></a>
<a href="/agente/legal"><div class="card">⚖️ Consulta Legal</div></a>
<a href="/agente/financiero"><div class="card">📊 Evaluación Financiera</div></a>
<a href="/agente/diagnostico"><div class="card">📋 Diagnóstico</div></a>

</div>

</div>

</body>
</html>

""")

# ================= AGENTE =================

@app.route("/agente/<tipo>", methods=["GET","POST"])
def agente(tipo):

    respuesta=""

    if request.method=="POST":

        consulta=request.form["consulta"]
        archivo=request.files.get("archivo")
        info=archivo.filename if archivo else ""

        prompt = roles[tipo] + f"""
Consulta:
{consulta}

Archivo:
{info}
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
margin:0;
font-family:Arial;
background:#f1f4f9;
}

.container{
width:80%;
margin:auto;
margin-top:40px;
background:white;
padding:30px;
border-radius:15px;
box-shadow:0 6px 18px rgba(0,0,0,0.1);
}

textarea{
width:100%;
height:160px;
border-radius:10px;
padding:10px;
border:1px solid #ccc;
}

button{
background:#0b2545;
color:white;
padding:12px 30px;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;
}

.result{
margin-top:25px;
background:#f4f6fb;
padding:20px;
border-radius:10px;
white-space:pre-wrap;
}

</style>

</head>

<body>

<div class="container">

<h2>Agente {{tipo}}</h2>

<form method="post" enctype="multipart/form-data">

<textarea name="consulta"></textarea><br><br>
<input type="file" name="archivo"><br><br>

<button>Consultar IA</button>

</form>

<div class="result">{{respuesta}}</div>

<br>
<a href="/">⬅ Volver</a>

</div>

</body>
</html>

""", tipo=tipo.upper(), respuesta=respuesta)

if __name__ == "__main__":
    app.run()
