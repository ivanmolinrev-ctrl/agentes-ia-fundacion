from flask import Flask, request, render_template_string
import os
from openai import OpenAI
import base64
from PIL import Image
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

historial = []

# ================= DASHBOARD BONITO =================

@app.route("/")
def panel():
    return render_template_string("""

<html>
<head>
<title>Agentes de IA FUNCREDES </title>

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

.content{
margin-left:260px;
padding:40px;
}

.cards{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
gap:25px;
}

.card{
background:white;
padding:35px;
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

a{
text-decoration:none;
color:black;
}

</style>

</head>

<body>

<div class="sidebar">
<div class="logo">FUNCREDES IA</div>
</div>

<div class="content">

<h1>Panel de Agentes Inteligentes</h1>

<div class="cards">

<a href="/chat/formulador"><div class="card">🤖 Formular Proyecto</div></a>
<a href="/chat/presupuestos"><div class="card">💰 Presupuesto Obra</div></a>
<a href="/chat/licitaciones"><div class="card">📑 Analizar Licitación</div></a>
<a href="/chat/legal"><div class="card">⚖️ Consulta Legal</div></a>
<a href="/chat/financiero"><div class="card">📊 Evaluación Financiera</div></a>
<a href="/chat/diagnostico"><div class="card">📋 Diagnóstico</div></a>

</div>

</div>

</body>
</html>

""")

# ================= CHAT EXTREMO =================

import PyPDF2
import pandas as pd

@app.route("/chat/<agente>", methods=["GET","POST"])
def chat(agente):

    respuesta=""
    texto_archivo=""
    imagen_base64=None

    if request.method=="POST":

        consulta=request.form["consulta"]
        archivos = request.files.getlist("files")

        for archivo in archivos:

            if archivo.filename.endswith((".jpg",".png",".jpeg")):

                imagen_bytes = archivo.read()
                imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

        if imagen_base64:

            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role":"system","content":roles[agente]},
                    {"role":"user","content":[
                        {"type":"text","text":consulta},
                        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{imagen_base64}"}}
                    ]}
                ]
            )

        else:

            prompt = roles[agente] + f"""
Consulta:
{consulta}
"""

            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role":"user","content":prompt}]
            )

        respuesta = completion.choices[0].message.content

        historial.append((consulta,respuesta))

    return render_template_string(TU_HTML_DE_CHAT, historial=historial, agente=agente.upper())
<html>
<head>

<style>

body{
margin:0;
font-family:Arial;
background:#0f172a;
color:white;
}

.top{
background:#020617;
padding:15px;
font-size:22px;
font-weight:bold;
}

.layout{
display:flex;
height:88vh;
}

.chat{
flex:3;
padding:20px;
overflow:auto;
}

.historial{
flex:1;
background:#020617;
padding:15px;
overflow:auto;
}

.msg-user{
background:#2563eb;
padding:12px;
border-radius:10px;
margin:10px;
text-align:right;
}

.msg-ia{
background:#1e293b;
padding:12px;
border-radius:10px;
margin:10px;
}

.input{
position:fixed;
bottom:0;
width:100%;
background:#020617;
padding:15px;
}

textarea{
width:60%;
height:60px;
border-radius:8px;
}

button{
padding:10px 25px;
border-radius:8px;
background:#2563eb;
color:white;
border:none;
}

.preview img{
max-width:120px;
margin:5px;
}

</style>

<script>

function previewImages(){
let preview=document.getElementById('preview')
preview.innerHTML=""
let files=document.getElementById('files').files

for(let i=0;i<files.length;i++){
let reader=new FileReader()
reader.onload=function(e){
preview.innerHTML+="<img src='"+e.target.result+"'>"
}
reader.readAsDataURL(files[i])
}
}

</script>

</head>

<body>

<div class="top">
Agente {{agente}}
<a href="/" style="color:white;margin-left:20px">⬅ Panel</a>
</div>

<div class="layout">

<div class="chat">

{% for c,r in historial %}
<div class="msg-user">{{c}}</div>
<div class="msg-ia">{{r}}</div>
{% endfor %}

</div>

<div class="historial">
<h3>Historial</h3>
{% for c,r in historial %}
<p>Consulta enviada</p>
{% endfor %}
</div>

</div>

<div class="input">

<form method="post" enctype="multipart/form-data">

<textarea name="consulta"></textarea>

<input type="file" id="files" multiple onchange="previewImages()">

<button>Enviar</button>

<div id="preview" class="preview"></div>

</form>

</div>

</body>
</html>

""", historial=historial, agente=agente.upper())

if __name__ == "__main__":
    app.run()
