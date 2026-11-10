# dados.py - leitura, validação, limpeza e análise dos dados (Pandas)
import pandas as pd
 
# ---------- Formato do CSV aceito pela aplicação ----------
# Colunas de entrada (X): nome -> (rótulo para o usuário, mínimo, máximo)
# Os mínimos e máximos servem para detectar "valores impossíveis".
COLUNAS_X = {
    "idade": ("Idade (anos)", 16, 70),
    "renda_mensal": ("Renda mensal", 500, 50000),
    "distancia_casa": ("Distância de casa até o trabalho (km)", 0, 100),
    "anos_empresa": ("Tempo na empresa (anos)", 0, 50),
    "satisfacao_trabalho": ("Satisfação com o trabalho (1 a 4)", 1, 4),
    "horas_extras": ("Faz horas extras? (0 = não, 1 = sim)", 0, 1),
}
INTEIROS = ["satisfacao_trabalho", "horas_extras"]   # estas colunas só aceitam números inteiros
ALVO = "saiu"  # y: 1 = o funcionário saiu da empresa, 0 = ficou
NOMES_X = list(COLUNAS_X.keys())
COLUNAS_OBRIGATORIAS = NOMES_X + [ALVO]
 
 
class ErroCSV(Exception):
    """Erro com mensagem amigável para mostrar ao usuário."""
    pass
 
 
def ler_csv(caminho):
    """Lê o CSV (aceita separador , ou ;) e valida o arquivo. Não altera o original."""
    try:
        df = pd.read_csv(caminho, encoding="utf-8-sig")
        if df.shape[1] == 1:          # provavelmente o separador é ponto e vírgula
            df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        raise ErroCSV("O arquivo está vazio.")
    except Exception:
        raise ErroCSV("Não consegui ler o arquivo. Envie um CSV válido (separado por vírgula ou ponto e vírgula).")
 
    if df.empty:
        raise ErroCSV("O arquivo não tem nenhuma linha de dados.")
 
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ErroCSV("Faltam as colunas obrigatórias: " + ", ".join(faltando) +
                      ". Colunas esperadas: " + ", ".join(COLUNAS_OBRIGATORIAS) + ".")
    return df[COLUNAS_OBRIGATORIAS].copy()   # fica só com as colunas usadas
