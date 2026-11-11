# graficos.py - gera os 3 gráficos e devolve como imagem em texto (base64) para o HTML
import base64
from io import BytesIO
from matplotlib.figure import Figure   # Figure não depende de janela, funciona bem com Flask
from dados import ALVO
 
COR_FICOU = "#4C9F70"
COR_SAIU = "#D9534F"
 
 
def _para_base64(fig):
    """Converte a figura em PNG e depois em texto, para colocar direto no <img>."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
 
 
def grafico_distribuicao(df):
    """1) DISTRIBUIÇÃO: histograma da renda mensal."""
    fig = Figure(figsize=(5.5, 3.8))
    ax = fig.subplots()
    ax.hist(df["renda_mensal"], bins=20, color="#4A78B5", edgecolor="white")
    ax.axvline(df["renda_mensal"].mean(), color="black", linestyle="--",
               label=f"média = {df['renda_mensal'].mean():.0f}")
    ax.set_title("Distribuição da renda mensal dos funcionários")
    ax.set_xlabel("Renda mensal")
    ax.set_ylabel("Quantidade de funcionários")
    ax.legend()
    return _para_base64(fig)


def grafico_comparacao(df):
    """2) COMPARAÇÃO: barras com a quantidade de funcionários por classe do alvo."""
    contagem = df[ALVO].value_counts().sort_index()
    fig = Figure(figsize=(5.5, 3.8))
    ax = fig.subplots()
    barras = ax.bar(["Ficou (0)", "Saiu (1)"],
                    [contagem.get(0, 0), contagem.get(1, 0)], color=[COR_FICOU, COR_SAIU])
    ax.bar_label(barras)
    ax.set_title("Funcionários que ficaram e que saíram")
    ax.set_ylabel("Quantidade de funcionários")
    return _para_base64(fig)
