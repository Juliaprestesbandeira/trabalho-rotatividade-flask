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
