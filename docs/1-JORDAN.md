# Pessoa A — Base e Entidades

**Arquivo:** `helpdesk_TRIO_NOMES.py`
**Você começa primeiro — todos dependem de você**

---

## Antes de começar

- [ ] Combinar com o time os nomes exatos das exceções antes de qualquer um escrever código
- [ ] Criar o arquivo `helpdesk_TRIO_NOMES.py` com o nome correto do trio no lugar de NOMES
- [ ] Adicionar os imports necessários no topo: `datetime`, `collections.deque`

---

## Bloco 1 — Exceções customizadas

- [ ] Criar a classe `ChamadoNaoEncontradoException` herdando de `Exception`
- [ ] Criar a classe `CapacidadeExcedidaException` herdando de `Exception`
- [ ] Criar a classe `TransicaoInvalidaException` herdando de `Exception`

---

## Bloco 2 — Classe `Chamado`

### Estrutura base
- [ ] Declarar atributo de classe `_contador = 0` para geração de número sequencial
- [ ] Declarar dicionário de classe `SLA_MAP` com os valores: critica=4h, alta=8h, media=24h, baixa=72h
- [ ] Declarar dicionário de classe `TRANSICOES` mapeando cada status para o conjunto de status permitidos a seguir

### Método `__init__`
- [ ] Validar se a prioridade recebida existe no `SLA_MAP`, lançando `ValueError` com mensagem clara se não existir
- [ ] Incrementar `_contador` e atribuir o valor ao atributo `numero`
- [ ] Definir `status` inicial como `'aberto'`
- [ ] Definir `data_abertura` como o momento atual com `datetime.now()`
- [ ] Calcular e atribuir `sla_horas` consultando o `SLA_MAP` pela prioridade
- [ ] Inicializar `tecnico` como `None`
- [ ] Inicializar `historico` como lista vazia

### Método `__str__`
- [ ] Retornar uma linha com: número, título, cliente, prioridade, status e tempo decorrido

### Método `tempo_decorrido`
- [ ] Retornar a diferença entre `datetime.now()` e `data_abertura` como `timedelta`

### Método `esta_em_atraso`
- [ ] Retornar `False` imediatamente se o status for `'resolvido'` ou `'fechado'`
- [ ] Converter o tempo decorrido para horas
- [ ] Retornar `True` se as horas passadas ultrapassarem `sla_horas`

### Método `registrar_acao`
- [ ] Receber `acao` e `responsavel` como parâmetros
- [ ] Adicionar ao `historico` um dicionário com: data atual em ISO, ação e responsável

### Método `alterar_status`
- [ ] Consultar o `TRANSICOES` para saber quais status são permitidos a partir do status atual
- [ ] Lançar `TransicaoInvalidaException` com mensagem descritiva se o novo status não for permitido
- [ ] Atualizar `self.status` para o novo valor
- [ ] Chamar `registrar_acao` registrando a mudança de status

### Método `to_dict`
- [ ] Retornar dicionário com todos os atributos serializáveis
- [ ] Converter `data_abertura` para string com `.isoformat()`
- [ ] Incluir `historico` como lista
- [ ] Incluir o resultado de `esta_em_atraso()` como campo `'em_atraso'`

---

## Bloco 3 — Classe `Tecnico`

### Estrutura base
- [ ] Declarar atributo de classe `_contador = 0` para geração de id sequencial

### Método `__init__`
- [ ] Incrementar `_contador` e atribuir ao `id_tecnico`
- [ ] Converter `especialidades` para `set` internamente, independente do tipo recebido
- [ ] Inicializar `chamados_ativos` como lista vazia
- [ ] Definir `disponivel` como `True` (começa sem chamados)

### Método `__str__`
- [ ] Retornar uma linha com: id, nome, especialidades, chamados ativos e disponibilidade

### Método `atribuir_chamado`
- [ ] Lançar `CapacidadeExcedidaException` se `disponivel` for `False`
- [ ] Adicionar o número do chamado à lista `chamados_ativos`
- [ ] Recalcular `disponivel` comparando `len(chamados_ativos) < capacidade_maxima`

### Método `liberar_chamado`
- [ ] Lançar `ValueError` com mensagem clara se o número não estiver em `chamados_ativos`
- [ ] Remover o número da lista `chamados_ativos`
- [ ] Recalcular `disponivel`

### Método `tem_especialidade`
- [ ] Retornar `True` se a categoria recebida estiver no set `especialidades`

### Método `to_dict`
- [ ] Retornar dicionário com todos os atributos
- [ ] Converter `especialidades` de `set` para `list` para ser serializável em JSON

---

## Bloco 4 — Bloco de demonstração

- [ ] Criar o bloco `if __name__ == '__main__':` no final do arquivo
- [ ] Instanciar `CentralDeSupporte("Ciesa Solutions")`
- [ ] Registrar no mínimo 4 técnicos com especialidades variadas
- [ ] Abrir no mínimo 8 chamados com prioridades e clientes diferentes
- [ ] Chamar `atribuicao_automatica()` e imprimir o resultado
- [ ] Resolver 2 chamados distintos com `resolver_chamado()`
- [ ] Fechar 1 chamado com `fechar_chamado()`
- [ ] Tentar uma transição de status inválida dentro de um `try/except` e imprimir mensagem amigável
- [ ] Simular atraso subtraindo horas de `data_abertura` de um chamado via `timedelta`
- [ ] Chamar `listar_em_atraso()` e imprimir os resultados
- [ ] Chamar `painel_operacional()` e imprimir o resultado final

---

## Antes de passar para a Pessoa B

- [ ] Confirmar que as 3 exceções têm exatamente os nomes: `ChamadoNaoEncontradoException`, `CapacidadeExcedidaException`, `TransicaoInvalidaException`
- [ ] Confirmar que o atributo do número do chamado se chama `numero`
- [ ] Confirmar que o atributo do id do técnico se chama `id_tecnico`
- [ ] Confirmar que o atributo de disponibilidade se chama `disponivel` e é booleano
- [ ] Confirmar que o status inicial de todo chamado é a string `'aberto'`
- [ ] Confirmar que `to_dict()` de `Chamado` e `Tecnico` funciona sem erros
- [ ] Rodar o arquivo diretamente com `python helpdesk_TRIO_NOMES.py` e verificar que o bloco `__main__` executa sem exceções inesperadas
- [ ] Passar o arquivo para a Pessoa B