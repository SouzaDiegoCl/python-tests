# Regras de contexto — atividade1

- Mantenha o código em Python 3.12 ou superior e use `uv` para executar o projeto.
- Trate `PRD.md` como especificação das regras atuais. Ao alterar uma regra de negócio, atualize o PRD e a documentação de uso no README.
- Preserve a representação de `Estabulo.equinos` como lista de IDs em texto em todo o código.
- Mantenha os erros de regra de negócio explícitos e sem alterações parciais no repositório quando uma operação falhar.
- Ao criar a suíte de testes, use Pytest com padrão AAA, `@pytest.mark.unit`, parametrização, EP, BVA e cenários de entradas inválidas. Isole o estado dos repositórios entre casos.
- A verificação final da atividade deve executar `uv run pytest -v` e `uv run pytest --cov=app --cov-branch --cov-report=term-missing` e atingir 100% de linhas e ramificações.
- Registre em `AI_USAGE.md` como a IA foi usada e quais verificações foram realmente executadas; mantenha um link no README. Não declare cobertura ou revisão humana antes de elas ocorrerem.
