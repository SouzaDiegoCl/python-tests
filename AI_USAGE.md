# Relatório de transparência do uso de IA

Este arquivo registra como a inteligência artificial foi usada no projeto da AT1 de Qualidade e Teste de Software. Ele permite que quem avalia o trabalho identifique a contribuição da ferramenta, as decisões aplicadas e as verificações feitas. Deve ser atualizado quando a IA participar de novas etapas.

## Ferramenta e insumos

- **Ferramenta:** OpenAI Codex, assistente de programação.
- **Insumos:** enunciado da atividade fornecido pelo autor, arquivos locais do projeto e instruções do autor nesta conversa.
- **Finalidade:** analisar a base do projeto, corrigir inconsistências pontuais, organizar os testes de integração, criar testes unitários e redigir documentação.

## Contribuições nesta etapa

| Atividade | Participação da IA |
| --- | --- |
| Análise inicial | Conferiu estrutura, configuração de `uv`/Pytest, regras existentes e lacunas em relação ao enunciado. |
| Código de domínio | Corrigiu a mensagem de raça inválida para produzir `ValueError` e ajustou a listagem para tratar `Estabulo.equinos` como lista de IDs em texto. |
| Especificação | Redigiu `PRD.md` com as regras implementadas, critérios de aceite e limites conhecidos. |
| Documentação e governança | Redigiu `README.md`, `AGENTS.md` e este relatório; acrescentou artefatos gerados pelo Pytest e pela cobertura ao `.gitignore`. |
| Organização dos testes | Reuniu valores de exemplo e limites das factories em `tests/constants.py`, ajustou imports e fixtures existentes e atualizou um teste de integração para a rota de listagem disponível. |
| Verificação da associação | Ajustou a asserção do teste para comparar o ID do equino com os IDs presentes nos objetos retornados por `GET /estabulos`. |
| Ampliação da integração | Acrescentou cenários de capacidade exata e excedida, duplicidade, referências inexistentes, valores limite, entradas inválidas e conversão de erros do serviço para respostas HTTP. Atualizou o PRD e o README para refletir o comportamento testado. |
| Testes unitários | Substituiu a cópia de fixtures em `tests/testes_unitarios.py` por testes de esquemas e serviço com repositórios novos por caso. Acrescentou a descoberta do arquivo ao Pytest e usou parametrização, partições de equivalência e valores limite. |

Nenhuma regra de negócio foi alterada nesta ampliação. O PRD passou a registrar as validações de capacidade e associação já presentes no serviço e os limites ainda não implementados, como formato da data de nascimento.

## Como o resultado foi conferido

- O código alterado foi lido e comparado com o comportamento descrito no `PRD.md`.
- Uma execução manual do serviço, com repositórios em memória separados, confirmou cadastro de um equino, associação por ID e listagem com `estabulo_id` preenchido.
- Uma execução manual com raça fora da lista confirmou `ValueError` e ausência de gravação do equino inválido.
- `uv run pytest -v` foi executado na análise inicial: encontrou **0 testes**, encerrou com código 5 e reportou **0% de cobertura**. Esse resultado não comprova qualidade ou cobertura do código.
- Após a organização dos testes, `uv run pytest -v` executou **1 teste**, com **1 aprovação**.
- `uv run pytest --cov=app --cov-branch --cov-report=term-missing` executou **1 teste**, com **1 aprovação**, e reportou **63% de cobertura total de linhas e ramificações**.
- Após o ajuste da associação, `uv run pytest -v` executou **4 testes**, todos aprovados; `uv run pytest --cov=app --cov-branch --cov-report=term-missing` confirmou os **4 testes aprovados** e **83% de cobertura total**.
- Após a ampliação dos cenários, `uv run pytest -v` executou **35 casos**, todos aprovados. `uv run pytest --cov=app --cov-branch --cov-report=term-missing` confirmou **35 aprovações** e **100% de cobertura de linhas e ramificações** em `app`.
- Após incluir os testes unitários, `uv run pytest tests/testes_unitarios.py -v --no-cov` executou **35 casos unitários**, todos aprovados. `uv run pytest -v` e `uv run pytest --cov=app --cov-branch --cov-report=term-missing` executaram **70 casos**, todos aprovados, com **100% de cobertura de linhas e ramificações** em `app`.

## Pendências de auditoria

- A suíte contém 35 casos de integração e 35 casos unitários. Os testes unitários usam repositórios novos em cada caso; três cenários de integração usam mock do serviço.
- A meta de 100% de linhas e ramificações foi atingida na execução acima. A cobertura mede execução de código e não substitui a revisão do comportamento esperado.
- A revisão final do código e da documentação pelo autor permanece pendente. Os resultados da IA devem ser conferidos antes da entrega acadêmica.
