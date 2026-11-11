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


def treinar_e_salvar():
    df, _ = limpar(ler_csv(ARQ_DADOS))
    X = df[NOMES_X]      # entradas
    y = df[ALVO]         # resposta que o modelo deve prever (NÃO entra em X)
    # Mesma divisão para todos os modelos -> comparação justa
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=PROPORCAO_TESTE, random_state=RANDOM_STATE, stratify=y)
    baseline = max(y_test.mean(), 1 - y_test.mean())   # acerto de quem chutasse sempre a classe mais comum
    resultados, modelos = [], {}
    for nome, modelo in criar_modelos().items():
        modelo.fit(X_train, y_train)                    # aprende SÓ com o treino
        y_pred = modelo.predict(X_test)                 # prevê o teste (que ele nunca viu)
        resultados.append({
            "modelo": nome,
            "acuracia_treino": round(accuracy_score(y_train, modelo.predict(X_train)), 3),
            "acuracia_teste": round(accuracy_score(y_test, y_pred), 3),
            "recall_saiu": round(recall_score(y_test, y_pred), 3),
            "precisao_saiu": round(precision_score(y_test, y_pred), 3),
            "matriz": confusion_matrix(y_test, y_pred).tolist(),   # [[VN, FP], [FN, VP]]
        })
        modelos[nome] = modelo
    # Escolha: maior recall de quem saiu (não deixar de ver quem vai sair); desempate pela acurácia no teste
    melhor = max(resultados, key=lambda r: (r["recall_saiu"], r["acuracia_teste"]))
    os.makedirs(os.path.dirname(ARQ_MODELO), exist_ok=True)
    joblib.dump(modelos[melhor["modelo"]], ARQ_MODELO)
    info = {
        "base": "data/rotatividade.csv", "linhas_usadas": len(df),
        "treino": len(X_train), "teste": len(X_test),
        "proporcao_teste": PROPORCAO_TESTE, "random_state": RANDOM_STATE,
        "baseline": round(baseline, 3),
        "teste_classe_0": int((y_test == 0).sum()), "teste_classe_1": int((y_test == 1).sum()),
        "modelo_escolhido": melhor["modelo"], "resultados": resultados,
        "versao_sklearn": sklearn.__version__,
        "treinado_em": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    with open(ARQ_RESULTADOS, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    return info


if __name__ == "__main__":
    info = treinar_e_salvar()
    print("Treino:", info["treino"], "| Teste:", info["teste"], "| Baseline:", info["baseline"])
    for r in info["resultados"]:
        print(r["modelo"], "-> acurácia teste:", r["acuracia_teste"], "| recall:", r["recall_saiu"],
              "| precisão:", r["precisao_saiu"], "| matriz:", r["matriz"])
    print("Modelo escolhido:", info["modelo_escolhido"])
