# Testes manuais
 
Todos feitos no navegador, com `python app.py` rodando.
 
| # | O que testar | Como | Resultado esperado |
|---|---|---|---|
| 1 | Página inicial | Abrir http://127.0.0.1:5000 | Aparece o formulário de upload e a lista de colunas esperadas |
| 2 | Análise do CSV de exemplo | Menu "Análise (exemplo)" | 1470 registros antes e depois da limpeza, 3 gráficos e 4 achados |
| 3 | Upload válido | Enviar `data/rotatividade.csv` | Mesma análise, com o nome do arquivo no título |
| 4 | Upload sem arquivo | Clicar em "Enviar e analisar" sem escolher arquivo | "Escolha um arquivo CSV antes de enviar." |
| 5 | Upload com extensão errada | Enviar o `README.md` | "O arquivo precisa ter extensão .csv." |
| 6 | CSV com colunas faltando | Enviar CSV só com as colunas `a,b` | Mensagem listando as colunas obrigatórias que faltam |
| 7 | CSV vazio | Enviar um CSV sem nada dentro | "O arquivo está vazio." |
| 8 | Comparação de modelos | Menu "Modelos" | Tabela com 3 modelos; Regressão Logística destacada (recall 0.766) |
| 9 | Previsão válida | idade 30, renda 2500, distância 20, tempo 1, satisfação 1, horas extras 1 | Tende a SAIR, probabilidade 88.9% |
| 10 | Previsão com campo vazio | Deixar a renda mensal em branco | "Preencha o campo 'Renda mensal'." |
| 11 | Previsão com texto | Digitar abc na idade | "O campo 'Idade (anos)' precisa ser um número." |
| 12 | Previsão fora da faixa | Renda mensal 999999 | "O campo 'Renda mensal' deve estar entre 500 e 50000." |
