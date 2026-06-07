# Pessoa A — Base e Entidades

**Arquivo:** `helpdesk_TRIO_NOMES.py`
**Você começa primeiro — todos dependem de você**

---

## Antes de começar

- [x] Combinar com o time os nomes exatos das exceções antes de qualquer um escrever código
- [x] Criar o arquivo `helpdesk_TRIO_NOMES.py` com o nome correto do trio no lugar de NOMES
- [x] Adicionar os imports necessários no topo: `datetime`, `collections.deque`

---

## Bloco 1 — Exceções customizadas

- [x] Criar a classe `ChamadoNaoEncontradoException` herdando de `Exception`
- [x] Criar a classe `CapacidadeExcedidaException` herdando de `Exception`
- [x] Criar a classe `TransicaoInvalidaException` herdando de `Exception`

---

## Bloco 2 — Classe `Chamado`

### Estrutura base
- [x] Declarar atributo de classe `_contador = 0` para geração de número sequencial
- [x] Declarar dicionário de classe `SLA_MAP` com os valores: critica=4h, alta=8h, media=24h, baixa=72h
- [x] Declarar dicionário de classe `TRANSICOES` mapeando cada status para o conjunto de status permitidos a seguir

### Método `__init__`
- [x] Validar se a prioridade recebida existe no `SLA_MAP`, lançando `ValueError` com mensagem clara se não existir
- [x] Incrementar `_contador` e atribuir o valor ao atributo `numero`
- [x] Definir `status` inicial como `'aberto'`
- [x] Definir `data_abertura` como o momento atual com `datetime.now()`
- [x] Calcular e atribuir `sla_horas` consultando o `SLA_MAP` pela prioridade
- [x] Inicializar `tecnico` como `None`
- [x] Inicializar `historico` como lista vazia

### Método `__str__`
- [x] Retornar uma linha com: número, título, cliente, prioridade, status e tempo decorrido

### Método `tempo_decorrido`
- [x] Retornar a diferença entre `datetime.now()` e `data_abertura` como `timedelta`

### Método `esta_em_atraso`
- [x] Retornar `False` imediatamente se o status for `'resolvido'` ou `'fechado'`
- [x] Converter o tempo decorrido para horas
- [x] Retornar `True` se as horas passadas ultrapassarem `sla_horas`

### Método `registrar_acao`
- [x] Receber `acao` e `responsavel` como parâmetros
- [x] Adicionar ao `historico` um dicionário com: data atual em ISO, ação e responsável

### Método `alterar_status`
- [x] Consultar o `TRANSICOES` para saber quais status são permitidos a partir do status atual
- [x] Lançar `TransicaoInvalidaException` com mensagem descritiva se o novo status não for permitido
- [x] Atualizar `self.status` para o novo valor
- [x] Chamar `registrar_acao` registrando a mudança de status

### Método `to_dict`
- [x] Retornar dicionário com todos os atributos serializáveis
- [x] Converter `data_abertura` para string com `.isoformat()`
- [x] Incluir `historico` como lista
- [x] Incluir o resultado de `esta_em_atraso()` como campo `'em_atraso'`

---

## Bloco 3 — Classe `Tecnico`

### Estrutura base
- [x] Declarar atributo de classe `_contador = 0` para geração de id sequencial

### Método `__init__`
- [x] Incrementar `_contador` e atribuir ao `id_tecnico`
- [x] Converter `especialidades` para `set` internamente, independente do tipo recebido
- [x] Inicializar `chamados_ativos` como lista vazia
- [x] Definir `disponivel` como `True` (começa sem chamados)

### Método `__str__`
- [x] Retornar uma linha com: id, nome, especialidades, chamados ativos e disponibilidade

### Método `atribuir_chamado`
- [x] Lançar `CapacidadeExcedidaException` se `disponivel` for `False`
- [x] Adicionar o número do chamado à lista `chamados_ativos`
- [x] Recalcular `disponivel` comparando `len(chamados_ativos) < capacidade_maxima`

### Método `liberar_chamado`
- [x] Lançar `ValueError` com mensagem clara se o número não estiver em `chamados_ativos`
- [x] Remover o número da lista `chamados_ativos`
- [x] Recalcular `disponivel`

### Método `tem_especialidade`
- [x] Retornar `True` se a categoria recebida estiver no set `especialidades`

### Método `to_dict`
- [x] Retornar dicionário com todos os atributos
- [x] Converter `especialidades` de `set` para `list` para ser serializável em JSON

---

## Bloco 4 — Bloco de demonstração

- [x] Criar o bloco `if __name__ == '__main__':` no final do arquivo
- [x] Instanciar `CentralDeSupporte("Ciesa Solutions")`
- [x] Registrar no mínimo 4 técnicos com especialidades variadas
- [x] Abrir no mínimo 8 chamados com prioridades e clientes diferentes
- [x] Chamar `atribuicao_automatica()` e imprimir o resultado
- [x] Resolver 2 chamados distintos com `resolver_chamado()`
- [x] Fechar 1 chamado com `fechar_chamado()`
- [x] Tentar uma transição de status inválida dentro de um `try/except` e imprimir mensagem amigável
- [x] Simular atraso subtraindo horas de `data_abertura` de um chamado via `timedelta`
- [x] Chamar `listar_em_atraso()` e imprimir os resultados
- [x] Chamar `painel_operacional()` e imprimir o resultado final

---

## Antes de passar para a Pessoa B

- [x] Confirmar que as 3 exceções têm exatamente os nomes: `ChamadoNaoEncontradoException`, `CapacidadeExcedidaException`, `TransicaoInvalidaException`
- [x] Confirmar que o atributo do número do chamado se chama `numero`
- [x] Confirmar que o atributo do id do técnico se chama `id_tecnico`
- [x] Confirmar que o atributo de disponibilidade se chama `disponivel` e é booleano
- [x] Confirmar que o status inicial de todo chamado é a string `'aberto'`
- [x] Confirmar que `to_dict()` de `Chamado` e `Tecnico` funciona sem erros
- [x] Rodar o arquivo diretamente com `python helpdesk_TRIO_NOMES.py` e verificar que o bloco `__main__` executa sem exceções inesperadas
- [x] Passar o arquivo para a Pessoa B