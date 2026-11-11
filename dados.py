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


def diagnostico(df):
    """Tabela simples: tipo e quantidade de valores ausentes de cada coluna."""
    return pd.DataFrame({
        "coluna": df.columns,
        "tipo": [str(t) for t in df.dtypes],
        "ausentes": df.isna().sum().values,
    })


def limpar(df):
    """Limpa os dados e devolve (df_limpo, log). O log lista cada transformação."""
    log = []
    df = df.copy()
    log.append(f"Tamanho original: {len(df)} linhas.")
    # 1) Converter tudo para número. Texto inválido vira NaN (ausente).
    for col in COLUNAS_OBRIGATORIAS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # 2) Remover duplicatas (linhas repetidas distorcem as estatísticas)
    n = len(df)
    df = df.drop_duplicates()
    log.append(f"Duplicatas removidas: {n - len(df)}.")
    # 3) Remover linhas com valores ausentes (poucas linhas; evita inventar dados)
    n = len(df)
    df = df.dropna()
    log.append(f"Linhas com valores ausentes ou não numéricos removidas: {n - len(df)}.")
    # 4) Remover valores impossíveis (fora da faixa plausível de cada coluna)
    n = len(df)
    for col, (_, minimo, maximo) in COLUNAS_X.items():
        df = df[(df[col] >= minimo) & (df[col] <= maximo)]
        if col in INTEIROS:                        # satisfação e horas extras não podem ter casa decimal
            df = df[df[col] == df[col].round()]
    log.append(f"Linhas com valores impossíveis removidas: {n - len(df)}.")
    # 5) O alvo precisa ser 0 ou 1
    n = len(df)
    df = df[df[ALVO].isin([0, 1])]
    df[ALVO] = df[ALVO].astype(int)
    log.append(f"Linhas com alvo diferente de 0/1 removidas: {n - len(df)}.")
    log.append(f"Tamanho final: {len(df)} linhas.")
    if len(df) < 30:
        raise ErroCSV("Depois da limpeza sobraram menos de 30 linhas. Confira os dados do arquivo.")
    if df[ALVO].nunique() < 2:
        raise ErroCSV("A coluna " + ALVO + " precisa ter exemplos de 0 e de 1.")
    return df, log