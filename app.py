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
 
def montar_analise(caminho, nome_arquivo):
    """Lê, limpa, analisa e gera os gráficos de um CSV. Devolve o dicionário para a página."""
    bruto = dados.ler_csv(caminho)                   # o arquivo original não é alterado
    diag = dados.diagnostico(bruto)
    limpo, log = dados.limpar(bruto)
    resumo = dados.analisar(limpo)
    return {
        "arquivo": nome_arquivo,
        "linhas_antes": len(bruto), "linhas_depois": len(limpo), "n_colunas": bruto.shape[1],
        "amostra": bruto.head(5).to_html(index=False, classes="tabela"),
        "diagnostico": diag.to_html(index=False, classes="tabela"),
        "log": log,
        "estatisticas": resumo["estatisticas"].to_html(classes="tabela"),
        "medias": resumo["medias"].to_html(classes="tabela"),
        "achados": resumo["achados"],
        "g1": graficos.grafico_distribuicao(limpo),
        "g2": graficos.grafico_comparacao(limpo),
        "g3": graficos.grafico_relacao(limpo),
    }
 
 
@app.route("/analise", methods=["GET", "POST"])
def analise():
    if request.method == "POST":                     # usuário enviou um CSV
        arquivo = request.files.get("arquivo")
        if arquivo is None or arquivo.filename == "":
            return render_template("index.html", colunas=dados.COLUNAS_OBRIGATORIAS,
                                   erro="Escolha um arquivo CSV antes de enviar.")
        if not arquivo.filename.lower().endswith(".csv"):
            return render_template("index.html", colunas=dados.COLUNAS_OBRIGATORIAS,
                                   erro="O arquivo precisa ter extensão .csv.")
        carimbo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(PASTA_UPLOADS, carimbo + ".csv")   # guarda o original intacto
        arquivo.save(caminho)
        nome = arquivo.filename
    else:                                            # GET: usa o CSV de exemplo
        caminho, nome = ARQ_EXEMPLO, "rotatividade.csv (exemplo)"
 
    try:
        resultado = montar_analise(caminho, nome)
    except dados.ErroCSV as e:
        return render_template("index.html", colunas=dados.COLUNAS_OBRIGATORIAS, erro=str(e))
    return render_template("analise.html", r=resultado)

def ler_resultados():
    with open(modelo.ARQ_RESULTADOS, encoding="utf-8") as f:
        return json.load(f)


@app.route("/modelos")
def modelos():
    return render_template("modelos.html", info=ler_resultados())


@app.route("/previsao", methods=["GET", "POST"])
def previsao():
    info = ler_resultados()
    valores, erro, resultado = {}, None, None
    if request.method == "POST":
        valores, erro = modelo.validar_formulario(request.form)
        if erro is None:
            classe, prob = modelo.prever(MODELO, valores)
            resultado = {"classe": classe, "prob": round(prob, 1)}
        valores = valores or request.form            # mantém o que foi digitado
    return render_template("previsao.html", campos=dados.COLUNAS_X, valores=valores,
                           erro=erro, resultado=resultado, info=info)

if __name__ == "__main__":
    # debug=False e use_reloader=False são necessários para rodar no IDLE
    app.run(debug=False, use_reloader=False)
