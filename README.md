# Rotatividade de Funcionários - Aplicação Web com Análise de Dados e Machine Learning
 
Trabalho Final de Tópicos Especiais em Ciência da Computação.
 
## Integrantes e responsabilidades
| Integrante | Responsabilidade |
|---|---|
| Geovana Rafaela Domachowski Silva | Limpeza e análise dos dados (`dados.py`); páginas de modelos e de previsão (`app.py` e templates) |
| Jean Lucas de Paula Cavalheiro | Modelo e previsão (`modelo.py`), treino e avaliação (`treinar.py`); roteiro da demonstração, testes manuais e versão entregue (`docs/`) |
| Miguel Brugnolo | Gráficos (`graficos.py`) e README |
| Júlia Prestes Bandeira | Estrutura do repositório, base de dados, leitura e validação do CSV (`dados.py`); página inicial, análise e upload (`app.py` e templates) |
 
## Problema
Com dados básicos de um funcionário, é possível prever se ele **vai sair (1)** ou **vai ficar (0)** na empresa? É um problema de **classificação** supervisionada.
 
## Dados
- Fonte: base "IBM HR Analytics Employee Attrition & Performance" (1470 funcionários, 35 colunas), uma base fictícia criada para aprendizado, disponível no Kaggle. O arquivo original é `WA_Fn-UseC_-HR-Employee-Attrition.csv`.
- Arquivo do projeto: `data/rotatividade.csv`, com 7 colunas escolhidas pelo grupo. O arquivo original não é versionado neste repositório (a pasta `data/original/` é ignorada pelo Git).
- Reprodução: coloque o arquivo original em `data/original/` e rode `python gerar_base.py`, que cria `data/rotatividade.csv`. O alvo `saiu` vale 1 quando `Attrition` é "Yes" e 0 quando é "No". A coluna `OverTime` ("Yes"/"No") virou `horas_extras` (1/0).
 
### Dicionário de dados (formato aceito no upload)
| Coluna | Papel | Significado (coluna original) | Faixa aceita |
|---|---|---|---|
| idade | X | idade em anos (`Age`) | 16 a 70 |
| renda_mensal | X | renda mensal (`MonthlyIncome`) | 500 a 50000 |
| distancia_casa | X | distância de casa até o trabalho em km (`DistanceFromHome`) | 0 a 100 |
| anos_empresa | X | tempo na empresa em anos (`YearsAtCompany`) | 0 a 50 |
| satisfacao_trabalho | X | satisfação com o trabalho, de 1 (baixa) a 4 (muito alta) (`JobSatisfaction`) | inteiro de 1 a 4 |
| horas_extras | X | faz horas extras: 1 = sim, 0 = não (`OverTime`) | só 0 ou 1 |
| saiu | y | 1 = saiu da empresa, 0 = ficou (`Attrition`) | só 0 ou 1 |
 
Todas as colunas de X são dados conhecidos antes de o funcionário sair. O alvo não entra em X. As colunas de identificação (`EmployeeNumber`) e as colunas constantes (`EmployeeCount`, `Over18`, `StandardHours`) foram excluídas, assim como as demais colunas da base original, para manter o modelo simples e as entradas compreensíveis.

## Instalação e execução
1. Instale o Python 3 e, no Prompt de Comando: `pip install -r requirements.txt`
2. Abra `app.py` no IDLE e aperte **F5** (ou rode `python app.py`).
3. Abra no navegador: http://127.0.0.1:5000
4. (Opcional) Abra `treinar.py` e aperte F5 para retreinar e ver os resultados no console. Se `models/modelo.pkl` não existir, o `app.py` treina sozinho ao iniciar.
 
## Estrutura
- `app.py`: rotas Flask e integração
- `gerar_base.py`: gera o CSV de exemplo a partir da base original
- `dados.py`: leitura, validação, limpeza e análise (Pandas)
- `graficos.py`: os 3 gráficos
- `modelo.py`: validação do formulário, carregamento e previsão
- `treinar.py`: treino, comparação e avaliação dos modelos
- `templates/`: páginas HTML
- `data/`: CSV de exemplo | `models/`: modelo salvo e resultados (gerados ao rodar) | `uploads/`: CSVs enviados (originais intactos)
- `docs/`: roteiro da demonstração e testes manuais
 
## Limpeza dos dados
Conversão para número, remoção de duplicatas, de linhas com valores ausentes/não numéricos e de valores impossíveis (fora das faixas da tabela acima, ou com casa decimal em `satisfacao_trabalho` e `horas_extras`). Remover (em vez de preencher) evita inventar dados. A tela de análise mostra o tamanho antes e depois e o registro de cada transformação. Na base de exemplo nada precisou ser removido (1470 linhas antes e depois). O CSV original nunca é modificado.
 
## Gráficos (3)
Histograma da renda mensal (distribuição), barras de funcionários que ficaram e que saíram (comparação) e boxplot do tempo de empresa por classe (relação). Cada um tem interpretação na própria página.

## Modelos e avaliação
- Divisão: `train_test_split`, 80% treino / 20% teste, `random_state=42`, `stratify=y` (1176 treino, 294 teste: 247 da classe 0 e 47 da classe 1). Mesma divisão para todos os modelos.
- O pré-processamento (padronização, quando necessária) fica dentro de um `Pipeline`, aprendido só no treino e salvo junto com o modelo.
- Só cerca de 16% dos funcionários saíram (classes desequilibradas), então os três modelos usam `class_weight="balanced"`, que dá mais peso a quem saiu.
- Métricas: acurácia no teste, recall e precisão de quem saiu, e matriz de confusão. Referência: chutar sempre "ficou" acertaria 84,0%, mas nunca encontraria ninguém que vai sair (recall zero).
 
| Modelo | Acurácia treino | Acurácia teste | Recall (saiu) | Precisão (saiu) |
|---|---|---|---|---|
| Regressão Logística | 0,703 | 0,697 | 0,766 | 0,316 |
| Árvore de Decisão (max_depth=3) | 0,793 | 0,745 | 0,574 | 0,329 |
| Random Forest (100 árvores, max_depth=4) | 0,816 | 0,786 | 0,574 | 0,386 |
 
**Escolha final: Regressão Logística.** Foi a que mais encontrou quem realmente saiu (36 de 47, recall 0,766), contra 27 de 47 das outras duas. A acurácia de treino (0,703) é próxima à de teste (0,697), sem sinal de overfitting. O erro mais grave é prever "ficou" para quem sai (falso negativo), pois o funcionário em risco passa despercebido; o custo é o maior número de falsos alarmes (78 funcionários previstos como "saiu" que ficaram), por isso a precisão é baixa (0,316).
 
## Limitações
Apenas 6 variáveis e uma base fictícia; só 47 exemplos de quem saiu no teste, então os números mudam com outro sorteio. A acurácia (0,697) fica abaixo do chute fixo (0,840), e dois em cada três alertas de saída são falsos alarmes. É um estudo didático e não deve ser usado para decidir sobre pessoas reais. O modelo fica fixo (treinado com `data/rotatividade.csv`); o CSV enviado atualiza apenas análises e gráficos.
 
## Ferramentas e autoria
Código desenvolvido com apoio da IA Claude (Anthropic), e revisado pelo grupo. Bibliotecas: Flask, Pandas, scikit-learn, Matplotlib, joblib.

## Versão entregue
A versão avaliada é a da tag `v1.0` (branch `main`). Alterações posteriores só com autorização do professor.
