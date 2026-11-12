# Roteiro da demonstração em sala
 
Antes de começar: abrir o projeto, rodar `python app.py` (ou F5 no IDLE) e abrir http://127.0.0.1:5000.
 
## 1. Contexto e dados
- Pergunta: com 6 dados básicos de um funcionário, dá para prever se ele vai sair (1) ou ficar (0) na empresa?
- Fonte: base IBM HR Analytics Employee Attrition (1470 funcionários, fictícia, para aprendizado). Alvo `saiu` = 1 quando `Attrition` é "Yes".
- X: idade, renda_mensal, distancia_casa, anos_empresa, satisfacao_trabalho, horas_extras. y: saiu. O y não entra em X, e identificadores foram excluídos.
 
## 2. Upload e análise
1. Na página inicial, enviar `data/rotatividade.csv`.
2. Mostrar a amostra, o diagnóstico das colunas e o registro da limpeza (1470 linhas antes e depois).
3. Explicar os 3 gráficos: histograma da renda mensal (distribuição), barras de quem ficou e quem saiu (comparação) e boxplot do tempo de empresa por classe (relação).
4. Ler os 4 achados da página e chamar atenção para as classes desequilibradas (16,1% saíram).
5. Enviar um arquivo inválido (por exemplo o `README.md`) e mostrar a mensagem de erro.
 
## 3. Modelo e previsão
1. Abrir "Modelos": 80% treino (1176) e 20% teste (294), `random_state=42`.
2. Comparar Regressão Logística, Árvore de Decisão e Random Forest: acurácia, recall e precisão de quem saiu e matriz de confusão.
3. Justificar a escolha: Regressão Logística (maior recall de quem saiu: 36 de 47) e explicar por que a acurácia sozinha engana (o chute fixo "ficou" acerta 84%).
4. Abrir "Previsão" e preencher: idade 30, renda mensal 2500, distância 20, tempo na empresa 1, satisfação 1, horas extras 1. Resultado esperado: tende a SAIR, 88.9%.
5. Mostrar um campo inválido (por exemplo renda mensal 999999) e a mensagem de erro.
6. Falar das limitações: base fictícia, 6 variáveis, muitos falsos alarmes (precisão 0,316), estudo didático que não deve decidir sobre pessoas reais.
