# Gerenciamento de equinos — QTS AT1

Projeto da atividade **Engenharia de Testes Unitários, Cobertura de Código e Governança de IA**. O domínio é um serviço de gerenciamento de equinos em um haras. A versão atual permite cadastrar equinos, listá-los e associá-los a estábulos que já estejam no repositório em memória. As regras e seus limites estão em [PRD.md](PRD.md).

## Estado atual

- O projeto usa `uv`, Python 3.14, FastAPI e Pydantic. A configuração de Pytest e `pytest-cov` já está em `pyproject.toml`.
- As regras de contexto para manutenção do projeto estão em [AGENTS.md](AGENTS.md).
- A pasta `tests/` ainda está vazia por decisão desta etapa. Não há resultado de testes nem cobertura de 100% para apresentar neste momento.
- O cadastro de estábulos por API, a validação de lotação e a sincronização de `quantidade_equinos` ainda não foram implementados.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `app/schemas.py` | Modelos e validações de entrada. |
| `app/service.py` | Regras de cadastro, listagem e associação. |
| `app/repository.py` | Repositórios em memória. |
| `app/main.py` | Endpoints FastAPI. |
| `PRD.md` | Requisitos e critérios de aceite da versão atual. |
| `AGENTS.md` | Regras de contexto para trabalho com IA. |
| `AI_USAGE.md` | Registro do uso de IA e das verificações realizadas. |
| `tests/` | Local reservado para a futura suíte de testes. |

## Pré-requisitos e execução

Instale o [`uv`](https://docs.astral.sh/uv/) e tenha Python 3.14 disponível. Na pasta `atividade1`, execute:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

A API estará em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

Exemplo de cadastro de equino:

```bash
curl -X POST http://127.0.0.1:8000/equinos \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Lua","idade":6,"raca":"LUSITANO","sexo":"FEMEA","data_nascimento":"2020-01-01","peso":450.0}'
```

Para listar os equinos cadastrados:

```bash
curl http://127.0.0.1:8000/equinos
```

Os dados ficam apenas na memória e são perdidos quando o processo é encerrado. A rota de associação pressupõe que um estábulo já tenha sido adicionado ao repositório; ainda não há rota para criá-lo.

## Testes e cobertura — próxima etapa

Os comandos exigidos na apresentação da atividade serão:

```bash
uv run pytest -v
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

Como ainda não existem arquivos de teste, o primeiro comando encontra **0 testes** e encerra com código 5. A meta de 100% de linhas e ramificações só poderá ser verificada depois da implementação da suíte. A configuração atual mede todo o pacote `app`, incluindo API, repositórios, esquemas e serviço.

## Transparência sobre o uso de IA

Foi usado o OpenAI Codex para revisar o projeto, corrigir inconsistências e ajudar a redigir a documentação. O que a ferramenta fez, como o resultado foi conferido e o que ainda depende de auditoria estão descritos em [AI_USAGE.md](AI_USAGE.md). A revisão final pelo autor e a suíte automatizada permanecem pendentes.

## Entrega da atividade

Para a submissão final, ainda será necessário implementar a suíte de testes, comprovar 100% de cobertura de linhas e ramificações, publicar o repositório no GitHub e gravar o vídeo individual de até quatro minutos com áudio e demonstração dos comandos acima. O repositório e o vídeo precisam estar acessíveis publicamente antes do prazo da disciplina.
