# Citizen Assist AI

Assistente digital de orientação ao cidadão, executado no terminal, feito em Python
para a Global Solution 2026.2 (Pensamento Computacional e Automação com Python - FIAP).

## Integrantes
- Guilherme Cedro - RM 571050
- Gabriel Gonçalves - RM 569189
- Gabriel Carvalho - RM 571381

## Público e problema escolhidos
**Público:** jovens no primeiro emprego.

**Problema:** muitos jovens não sabem como tirar CPF, título de eleitor ou carteira de
trabalho digital, nem quais são seus direitos ao começar a trabalhar. A informação existe,
mas está espalhada e em linguagem técnica. O assistente responde essas dúvidas com
informações de fontes oficiais, mostrando a fonte, a data de verificação e um aviso,
sem coletar dados pessoais.

## ODS relacionados
- ODS 8 - Trabalho decente e crescimento econômico
- ODS 16 - Paz, justiça e instituições eficazes (acesso à informação)

## Como executar
1. Instale o Python 3.
2. Baixe ou clone este repositório.
3. No terminal, dentro da pasta do projeto, rode:

   python main.py

Não é preciso instalar nenhuma biblioteca externa.

## Estrutura
- `main.py`: menu principal.
- `orientacao.py`: classe `Orientacao` (um registro da base).
- `base_conhecimento.py`: classe `BaseConhecimento` (lê o JSON, lista categorias, busca com pontuação).
- `assistente.py`: classe `Assistente` (atendimento, histórico, indicadores e CSV).
- `data/base_conhecimento.json`: base com 12 orientações e 3 categorias (Documentos, Trabalho, Direitos).
- `data/historico.json`: histórico dos atendimentos (gerado pelo programa).
- `data/atendimentos.csv`: atendimentos exportados (gerado pelo programa).

## Regra de pontuação
A pergunta e as palavras-chave são normalizadas (minúsculas, sem acentos e sem pontuação).

| Regra | Resultado |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 pontos |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 ponto |
| Melhor orientação com 6 pontos ou mais | Confiança ALTA |
| Melhor orientação com 3 a 5 pontos | Confiança MÉDIA |
| Nenhuma orientação com 3 pontos | "Não encontrei" |

O método `buscar()` devolve uma lista de tuplas `(pontos, orientacao)` da maior para a menor
pontuação. O assistente mostra a melhor orientação e até duas alternativas.
Usamos exatamente os pesos e limites sugeridos no enunciado.

## Indicadores
- Resposta encontrada (%): atendimentos em que uma orientação foi encontrada, sobre o total.
- Taxa de acerto (%): atendimentos em que o usuário respondeu "s" (ajudou), sobre o total.
- Tempo médio para encontrar: média do tempo dos atendimentos em que a resposta foi encontrada.
- Tentativas por atendimento: média de perguntas feitas até achar (ou desistir).
- Facilidade de uso: média das notas de 1 a 5 dadas ao sair.
- Lista de dúvidas sem solução: perguntas não encontradas ou que não ajudaram.

## Integrações com outras disciplinas
Não houve integração com outras disciplinas.

## Fontes consultadas
- https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
- https://www.gov.br/pt-br/servicos/inscrever-no-cpf
- https://www.tse.jus.br/comunicacao/noticias/2022/Dezembro/ainda-nao-tem-titulo-de-eleitor-emita-o-documento-de-forma-gratuita-e-sem-sair-de-casa
- https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br
- https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/carteira-de-trabalho/perguntas-frequentes-carteira-de-trabalho-digital/
- https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/aprendizagem-profissional
- https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine
- https://www.gov.br/pt-br/servicos/alistar-se-no-servico-militar-obrigatorio
- https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm
- https://www.caixa.gov.br/beneficios-trabalhador/fgts/Paginas/default.aspx
- https://www.gov.br/pt-br/servicos/emitir-extrato-de-contribuicao-cnis
- https://mpt.mp.br/pgt/servicos/servico-denuncie



## Resultado do teste com usuários
(PREENCHER depois de testar com pelo menos 3 pessoas de fora do grupo, somando 10 atendimentos ou mais.
Não escreva nomes nem dados das pessoas.)

- Número de pessoas: 
- Número de atendimentos: 
- Resposta encontrada (%): 
- Taxa de acerto (%): 
- Tempo médio para encontrar: 
- Tentativas por atendimento: 
- Facilidade de uso (1 a 5): 
- Dúvidas sem solução: 
- Melhoria feita a partir do teste: 

## Limitações
- O assistente só responde com o que está na base de conhecimento (12 orientações).
- A busca é por palavras-chave: se a pessoa usar palavras diferentes das cadastradas, pode não encontrar.
- Não entende erros de digitação.
- As informações podem mudar; confira sempre o site oficial indicado na resposta.
- Este assistente não é um canal oficial.
- A nota de facilidade só é pedida ao sair se houve atendimento na sessão.

## Link do vídeo
(colocar o link do YouTube aqui)