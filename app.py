# app.py - aplicação Flask: define as páginas (rotas) e liga tudo
import os
import json
import datetime
from flask import Flask, render_template, request
import dados
import graficos
import modelo
 
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ_EXEMPLO = os.path.join(PASTA, "data", "rotatividade.csv")
PASTA_UPLOADS = os.path.join(PASTA, "uploads")
os.makedirs(PASTA_UPLOADS, exist_ok=True)
 
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024   # limite de 5 MB por arquivo
 
MODELO = modelo.carregar_modelo()                    # carrega (ou treina) uma vez ao iniciar
 
 
@app.route("/")
def index():
    return render_template("index.html", colunas=dados.COLUNAS_OBRIGATORIAS, erro=None)
 
 
if __name__ == "__main__":
    # debug=False e use_reloader=False são necessários para rodar no IDLE
    app.run(debug=False, use_reloader=False)
