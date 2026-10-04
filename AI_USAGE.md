# Relatório de transparência do uso de IA

Este arquivo registra como a inteligência artificial foi usada no projeto da AT1 de Qualidade e Teste de Software. Ele permite que quem avalia o trabalho identifique a contribuição da ferramenta, as decisões aplicadas e as verificações feitas. Deve ser atualizado quando a IA participar de novas etapas.

## Ferramenta e insumos

- **Ferramenta:** OpenAI Codex, assistente de programação.
- **Insumos:** enunciado da atividade fornecido pelo autor, arquivos locais do projeto e instruções do autor nesta conversa.
- **Finalidade:** analisar a base do projeto, corrigir inconsistências pontuais e redigir documentação. A IA ainda não foi usada para gerar a suíte de testes desta atividade.

## Contribuições nesta etapa

| Atividade | Participação da IA |
| --- | --- |
| Análise inicial | Conferiu estrutura, configuração de `uv`/Pytest, regras existentes e lacunas em relação ao enunciado. |
| Código de domínio | Corrigiu a mensagem de raça inválida para produzir `ValueError` e ajustou a listagem para tratar `Estabulo.equinos` como lista de IDs em texto. |
| Especificação | Redigiu `PRD.md` com as regras implementadas, critérios de aceite e limites conhecidos. |
| Documentação e governança | Redigiu `README.md`, `AGENTS.md` e este relatório; acrescentou artefatos gerados pelo Pytest e pela cobertura ao `.gitignore`. |

Nenhuma nova regra de validação foi adicionada nesta etapa. O PRD distingue as regras em funcionamento das validações ainda não implementadas, como lotação do estábulo, peso e formato da data de nascimento.

## Como o resultado foi conferido

- O código alterado foi lido e comparado com o comportamento descrito no `PRD.md`.
- Uma execução manual do serviço, com repositórios em memória separados, confirmou cadastro de um equino, associação por ID e listagem com `estabulo_id` preenchido.
- Uma execução manual com raça fora da lista confirmou `ValueError` e ausência de gravação do equino inválido.
- `uv run pytest -v` foi executado na análise inicial: encontrou **0 testes**, encerrou com código 5 e reportou **0% de cobertura**. Esse resultado não comprova qualidade ou cobertura do código.

## Pendências de auditoria

- A suíte automatizada de testes ainda não foi criada, conforme orientação do autor para esta etapa.
- A meta de 100% de linhas e ramificações ainda não foi verificada.
- A revisão final do código e da documentação pelo autor permanece pendente. Os resultados da IA devem ser conferidos antes da entrega acadêmica.
