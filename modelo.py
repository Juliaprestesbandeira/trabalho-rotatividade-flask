# modelo.py - preparação, carregamento do modelo e previsão
import os
import joblib
import pandas as pd

from dados import COLUNAS_X, NOMES_X, INTEIROS

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ_MODELO = os.path.join(PASTA, "models", "modelo.pkl")
ARQ_RESULTADOS = os.path.join(PASTA, "models", "resultados.json")

def carregar_modelo():
    """Carrega o modelo salvo. Se não existir (ou for incompatível), treina de novo."""
    try:
        return joblib.load(ARQ_MODELO)
    except Exception:
        import treinar          # importa aqui para evitar import circular
        treinar.treinar_e_salvar()
        return joblib.load(ARQ_MODELO)

def validar_formulario(form):
    """Confere os campos do formulário. Devolve (valores, mensagem_de_erro)."""
    valores = {}
    for nome, (rotulo, minimo, maximo) in COLUNAS_X.items():
        texto = form.get(nome, "").strip().replace(",", ".")
        if texto == "":
            return None, f"Preencha o campo '{rotulo}'."
        try:
            numero = float(texto)
        except ValueError:
            return None, f"O campo '{rotulo}' precisa ser um número."
        if numero < minimo or numero > maximo:
            return None, f"O campo '{rotulo}' deve estar entre {minimo} e {maximo}."
        if nome in INTEIROS and numero != int(numero):
            return None, f"O campo '{rotulo}' precisa ser um número inteiro."
        valores[nome] = numero
    return valores, None

def prever(modelo, valores):
    """Monta UMA linha com as mesmas colunas (e ordem) do treino e chama predict()."""
    linha = pd.DataFrame([valores], columns=NOMES_X)
    classe = int(modelo.predict(linha)[0])
    prob_saida = float(modelo.predict_proba(linha)[0][1]) * 100
    return classe, prob_saida