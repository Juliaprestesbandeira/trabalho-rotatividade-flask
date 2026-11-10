# gerar_base.py - cria data/rotatividade.csv a partir da base original IBM HR Analytics (Attrition)
# Antes de rodar: coloque o arquivo original WA_Fn-UseC_-HR-Employee-Attrition.csv na pasta data/original/
# Para rodar: python gerar_base.py
import os
import sys
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIGINAL = os.path.join(PASTA, "data", "original", "WA_Fn-UseC_-HR-Employee-Attrition.csv")
DESTINO = os.path.join(PASTA, "data", "rotatividade.csv")

if not os.path.exists(ORIGINAL):
    print("Arquivo original nao encontrado:", ORIGINAL)
    print("Baixe a base IBM HR Analytics Employee Attrition e coloque o arquivo na pasta data/original/")
    sys.exit(1)

bruto = pd.read_csv(ORIGINAL, encoding="utf-8-sig")

# Ficam só 6 colunas de entrada (X) e o alvo (y). Identificadores (EmployeeNumber) e colunas
# constantes (EmployeeCount, Over18, StandardHours) não entram.
base = pd.DataFrame({
    "idade": bruto["Age"],
    "renda_mensal": bruto["MonthlyIncome"],
    "distancia_casa": bruto["DistanceFromHome"],
    "anos_empresa": bruto["YearsAtCompany"],
    "satisfacao_trabalho": bruto["JobSatisfaction"],
    "horas_extras": (bruto["OverTime"] == "Yes").astype(int),   # Yes -> 1, No -> 0
    "saiu": (bruto["Attrition"] == "Yes").astype(int),          # Yes -> 1 (saiu), No -> 0 (ficou)
})

os.makedirs(os.path.join(PASTA, "data"), exist_ok=True)
base.to_csv(DESTINO, index=False)
print("Arquivo criado: data/rotatividade.csv com", len(base), "linhas")