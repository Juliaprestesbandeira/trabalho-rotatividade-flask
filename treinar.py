# treinar.py - treina, compara 3 modelos, avalia e salva o melhor
# Para rodar: abra no IDLE e aperte F5 (o app.py também chama isto sozinho se faltar o modelo).

import os
import json
import datetime
import joblib
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix
from dados import ler_csv, limpar, NOMES_X, ALVO
from modelo import ARQ_MODELO, ARQ_RESULTADOS, PASTA

ARQ_DADOS = os.path.join(PASTA, "data", "rotatividade.csv")
PROPORCAO_TESTE = 0.20     # 80% treino / 20% teste
RANDOM_STATE = 42          # fixa o sorteio para o resultado ser sempre o mesmo

def criar_modelos():
    """Os 3 modelos comparados. O Pipeline guarda o pré-processamento junto com o modelo.
    class_weight="balanced": só cerca de 16% dos funcionários saíram, então damos mais peso a quem saiu."""
    return {
        "Regressão Logística": Pipeline([("escala", StandardScaler()),
                                         ("modelo", LogisticRegression(max_iter=1000, class_weight="balanced"))]),
        "Árvore de Decisão": Pipeline([("modelo", DecisionTreeClassifier(max_depth=3, class_weight="balanced",
                                                                          random_state=RANDOM_STATE))]),
        "Random Forest": Pipeline([("modelo", RandomForestClassifier(n_estimators=100, max_depth=4,
                                                                      class_weight="balanced",
                                                                      random_state=RANDOM_STATE))]),
    }