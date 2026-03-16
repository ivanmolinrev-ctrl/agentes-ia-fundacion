from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    return "Sistema de Agentes IA funcionando 🚀"

if __name__ == "__main__":
    app.run()
