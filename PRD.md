# PRD — Gerenciamento de equinos

## Objetivo e escopo

Esta versão oferece um serviço em Python para cadastrar equinos, listá-los e associá-los a estábulos existentes. O domínio é determinístico: dados válidos são aceitos conforme as regras abaixo, e uma raça fora da lista é rejeitada. Os repositórios mantêm os registros apenas em memória; não há banco de dados.

O escopo deste PRD descreve o comportamento implementado nesta etapa. A suíte de testes unitários será criada em uma etapa posterior.

## Dados do domínio

| Entidade | Campos e regras atuais |
| --- | --- |
| Equino | `id` gerado como UUID em texto; `nome` de 1 a 200 caracteres; `idade` inteira maior ou igual a zero; `raca` não vazia e pertencente à lista aceita; `sexo` igual a `MACHO` ou `FEMEA`; `peso` numérico; `data_nascimento` em texto; `estabulo_id` opcional. |
| Estábulo | `id`, nome identificador, localização, capacidade, quantidade de equinos e `equinos`, uma lista de **IDs em texto**. O esquema `CriarEstabulo` exige nome de 1 a 200 caracteres, localização não vazia, capacidade maior que zero e quantidade inicial maior ou igual a zero. Ainda não existe operação pública para cadastrar estábulos. |

## Regras de negócio e critérios de aceite

### RN01 — Cadastro de equino

- A entrada é validada pelo esquema `CriarEquino` antes de chegar ao serviço.
- As raças aceitas são `MANGA-LARGA MARCHADOR`, `QUARTO DE MILHA`, `ANDALUZ` e `LUSITANO`. A comparação ignora diferenças entre maiúsculas e minúsculas; o valor recebido é preservado no cadastro.
- Para uma raça aceita, o serviço gera um ID, grava o equino no repositório e devolve o registro criado.
- Para uma raça não aceita, o serviço lança `ValueError` com a raça recebida e as opções válidas; nenhum equino é gravado. Na API, esse erro é convertido em HTTP 400.

### RN02 — Listagem de equinos

- A listagem retorna todos os equinos presentes no repositório.
- Para cada ID presente na lista `equinos` de um estábulo, se existir um equino com esse ID, seu `estabulo_id` é preenchido com o ID do estábulo.
- Um ID de equino inexistente na lista de um estábulo é ignorado durante a listagem.

### RN03 — Associação a estábulo

- A associação exige um equino e um estábulo já cadastrados nos respectivos repositórios.
- Se o equino não existir, o serviço lança `ValueError`. Se o estábulo não existir, o serviço também lança `ValueError`. Na API, esses erros são convertidos em HTTP 400.
- Em uma associação bem-sucedida, `equino.estabulo_id` recebe o ID do estábulo, e a lista `estabulo.equinos` recebe **somente o ID do equino**.

## Limites desta versão

- Não há endpoint para criar, editar ou remover estábulos, nem persistência além da memória do processo.
- A capacidade do estábulo, associações repetidas e transferências entre estábulos ainda não são validadas pelo serviço. O campo `quantidade_equinos` ainda não é sincronizado automaticamente com a lista de IDs.
- `peso` não tem limite de negócio definido, e `data_nascimento` ainda não tem validação de formato ou coerência com `idade`. Essas regras exigem definição antes de serem incluídas nos testes como comportamento obrigatório.

## Orientação para a futura suíte de testes

- **Particionamento de equivalência:** raça aceita/inválida; sexo aceito/inválido; IDs existentes/inexistentes; estábulo com ID de equino existente/inexistente.
- **Análise de valor limite:** nome com 0, 1, 200 e 201 caracteres; idade com -1, 0 e 1; capacidade de criação do estábulo com 0 e 1.
- **Error guessing:** dados ausentes, raça vazia, referências inexistentes e estado em memória isolado entre cenários.
- Os testes serão escritos com Pytest, padrão AAA, parametrização e marcação `unit`. A meta da atividade é 100% de cobertura de linhas e ramificações em `app`.
