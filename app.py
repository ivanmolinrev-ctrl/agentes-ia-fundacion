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

historial = []

@app.route("/")
def panel():
    return """
    <h1 style='font-family:Arial'>Plataforma IA FUNCREDES</h1>
    <a href='/chat/formulador'>Formulador</a><br>
    <a href='/chat/presupuestos'>Presupuestos</a><br>
    <a href='/chat/licitaciones'>Licitaciones</a><br>
    <a href='/chat/legal'>Legal</a><br>
    <a href='/chat/financiero'>Financiero</a><br>
    <a href='/chat/diagnostico'>Diagnóstico</a>
    """

@app.route("/chat/<agente>", methods=["GET","POST"])
def chat(agente):

    respuesta=""

    if request.method=="POST":

        consulta=request.form["consulta"]

        prompt = roles[agente] + f"\nConsulta:{consulta}"

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role":"user","content":prompt}]
        )

        respuesta = completion.choices[0].message.content

        historial.append((consulta,respuesta))

    return render_template_string("""

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
height:90vh;
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
width:75%;
background:#020617;
padding:15px;
}

textarea{
width:70%;
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
FUNCREDES IA — Agente {{agente}}
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
<p>Consulta</p>
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
