# PRD — Gerenciamento de equinos

## Objetivo e escopo

Esta versão oferece um serviço em Python para cadastrar e listar equinos e estábulos, além de associar equinos a estábulos. Dados válidos são aceitos conforme as regras abaixo, e uma raça fora da lista é rejeitada. Os repositórios mantêm os registros apenas em memória; não há banco de dados.

O escopo deste PRD descreve o comportamento implementado nesta etapa. A suíte atual cobre a API com testes de integração e as regras do domínio com testes unitários isolados.

## Dados do domínio

| Entidade | Campos e regras atuais |
| --- | --- |
| Equino | `id` gerado como UUID em texto; `nome` de 1 a 200 caracteres; `idade` inteira maior ou igual a zero; `raca` não vazia e pertencente à lista aceita; `sexo` igual a `MACHO` ou `FEMEA`; `peso` numérico; `data_nascimento` em texto; `estabulo_id` opcional. |
| Estábulo | `id`, nome identificador, localização, capacidade e `equinos`, uma lista de **IDs em texto** no repositório. O esquema `CriarEstabulo` exige nome de 1 a 200 caracteres, localização não vazia e capacidade maior que zero. A API permite cadastrar e listar estábulos. |

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
- Em uma associação bem-sucedida, a lista `estabulo.equinos` recebe **somente o ID do equino**. A listagem de equinos preenche `estabulo_id` na resposta com base nessa associação.
- Um estábulo aceita associações até sua capacidade, inclusive. A tentativa seguinte retorna HTTP 400 por capacidade máxima, sem acrescentar o equino ao estábulo. A criação do equino continua permitida independentemente da capacidade de um estábulo.
- Associar novamente o mesmo equino ao mesmo estábulo retorna HTTP 400, sem duplicar o ID. IDs de equino ou estábulo inexistentes também retornam HTTP 400.

### RN04 — Cadastro e listagem de estábulos

- O cadastro aceita uma capacidade inteira maior que zero e devolve o estábulo criado com ID gerado.
- A listagem retorna os estábulos e expande os IDs válidos da lista `equinos` em objetos de equino. Referências a equinos inexistentes são ignoradas na resposta; o repositório mantém somente IDs em texto.

## Limites desta versão

- Não há endpoint para editar ou remover estábulos, nem persistência além da memória do processo.
- Transferências entre estábulos ainda não são validadas pelo serviço. O campo `quantidade_equinos` do esquema de edição não é sincronizado automaticamente com a lista de IDs.
- `peso` não tem limite de negócio definido, e `data_nascimento` ainda não tem validação de formato ou coerência com `idade`. Essas regras exigem definição antes de serem incluídas nos testes como comportamento obrigatório.

## Critérios para ampliar a suíte de testes

- **Particionamento de equivalência:** raça aceita/inválida; sexo aceito/inválido; IDs existentes/inexistentes; estábulo com ID de equino existente/inexistente.
- **Análise de valor limite:** nome com 0, 1, 200 e 201 caracteres; idade com -1, 0 e 1; capacidade de criação do estábulo com 0 e 1.
- **Error guessing:** dados ausentes, raça vazia, referências inexistentes e estado em memória isolado entre cenários.
- A suíte usa Pytest, padrão AAA, parametrização e as marcações `integration` e `unit`. A meta da atividade é 100% de cobertura de linhas e ramificações em `app`.
