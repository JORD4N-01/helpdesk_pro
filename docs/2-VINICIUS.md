# Pessoa B — Lógica de Negócio

**Arquivo:** `helpdesk_TRIO_NOMES.py` (mesmo arquivo da Pessoa A)
**Aguardar a Pessoa A terminar e passar o arquivo antes de começar**

---

## Antes de começar

- [x] Receber o arquivo da Pessoa A e verificar que ele roda sem erros com `python helpdesk_TRIO_NOMES.py`
- [x] Confirmar com a Pessoa A os nomes exatos das exceções, atributos e o que `to_dict()` retorna
- [x] Verificar que `from collections import deque` já está nos imports, adicionar se não estiver
- [x] Adicionar `from collections import Counter` nos imports

---

## Bloco 1 — Estrutura da `CentralDeSupporte`

### Método `__init__`
- [x] Receber `empresa` como parâmetro e salvar no atributo
- [x] Criar `self.chamados` como `dict` vazio — justificativa: hash table garante busca O(1) mesmo com milhares de registros, requisito crítico do projeto
- [x] Criar `self.tecnicos` como `dict` vazio
- [x] Criar `self.fila_nao_atribuidos` como `deque()` vazia — justificativa: `popleft()` é O(1), enquanto `list.pop(0)` seria O(n)

### Método `abrir_chamado`
- [x] Criar um objeto `Chamado` com os parâmetros recebidos
- [x] Armazenar o chamado em `self.chamados` usando o número do chamado como chave
- [x] Adicionar o número à `fila_nao_atribuidos` com `append`
- [x] Retornar o objeto criado

### Método `registrar_tecnico`
- [x] Criar um objeto `Tecnico` com os parâmetros recebidos
- [x] Armazenar em `self.tecnicos` usando o `id_tecnico` como chave
- [x] Retornar o objeto criado

---

## Bloco 2 — Busca

### Método `buscar_chamado`
- [x] Tentar recuperar o chamado do dicionário `self.chamados` pelo número
- [x] Lançar `ChamadoNaoEncontradoException` com mensagem clara se o número não existir
- [x] Retornar o objeto `Chamado` encontrado
- [x] **Atenção:** este é o método que justifica o uso de `dict` — o professor vai perguntar sobre ele

---

## Bloco 3 — Atribuição manual

### Método `atribuir_tecnico`
- [x] Buscar o chamado pelo número usando `buscar_chamado()` (já trata o 404)
- [x] Verificar se o `id_tecnico` existe em `self.tecnicos`, lançar `ChamadoNaoEncontradoException` se não existir
- [x] Chamar `tecnico.atribuir_chamado(numero)` — o método da Pessoa A já lança `CapacidadeExcedidaException` se necessário
- [x] Atribuir o `id_tecnico` ao atributo `chamado.tecnico`
- [x] Chamar `chamado.alterar_status('em_atendimento', nome_do_tecnico)`
- [x] Registrar no histórico que o chamado foi atribuído ao técnico
- [x] Remover o número da `fila_nao_atribuidos` se ainda estiver nela

---

## Bloco 4 — Atribuição automática

### Método `atribuicao_automatica`
- [x] Criar uma deque auxiliar para chamados que não puderam ser atribuídos
- [x] Percorrer a fila com `popleft()` enquanto houver itens
- [x] Para cada chamado, filtrar apenas os técnicos com `disponivel == True`
- [x] Se não houver técnico disponível, recolocar o chamado na deque auxiliar e continuar
- [x] Selecionar o técnico com menor quantidade de chamados ativos — em caso de empate, escolher o de menor `id_tecnico`
- [x] Realizar a atribuição: chamar `atribuir_chamado`, atualizar `chamado.tecnico`, mudar status para `'em_atendimento'` e registrar no histórico como ação do sistema
- [x] Incrementar um contador a cada atribuição realizada
- [x] Ao final, substituir `fila_nao_atribuidos` pela deque auxiliar com os não atribuídos
- [x] Retornar o contador com a quantidade total de chamados atribuídos

---

## Bloco 5 — Resolução e fechamento

### Método `resolver_chamado`
- [x] Buscar o chamado pelo número usando `buscar_chamado()`
- [x] Verificar se `chamado.tecnico` é igual ao `id_tecnico` recebido
- [x] Lançar `PermissionError` com mensagem clara se o técnico não for o responsável — **a Pessoa C usa esta exceção para retornar HTTP 403**
- [x] Chamar `chamado.alterar_status('resolvido', nome_do_tecnico)`
- [x] Registrar a descrição da solução no histórico do chamado
- [x] Chamar `tecnico.liberar_chamado(numero)` para liberar o técnico

### Método `fechar_chamado`
- [x] Buscar o chamado pelo número usando `buscar_chamado()`
- [x] Chamar `chamado.alterar_status('fechado', 'sistema')` — a validação de transição já está no `alterar_status` da Pessoa A

---

## Bloco 6 — Relatórios

### Método `listar_em_atraso`
- [x] Filtrar todos os chamados do dicionário onde `esta_em_atraso()` retorna `True`
- [x] Ordenar a lista pelo tempo decorrido de forma decrescente (mais atrasado primeiro)
- [x] Retornar a lista ordenada de objetos `Chamado`

### Método `relatorio_por_prioridade`
- [x] Criar um dicionário com as quatro chaves de prioridade como listas vazias
- [x] Percorrer os chamados e agrupar os que não estão resolvidos nem fechados pela prioridade
- [x] Retornar o dicionário com listas de chamados serializados com `to_dict()`

### Método `painel_operacional`
- [x] Contar quantos chamados existem em cada status usando `Counter`
- [x] Obter a quantidade de chamados em atraso chamando `listar_em_atraso()`
- [x] Listar os técnicos disponíveis serializados com `to_dict()`
- [x] Identificar os 3 clientes com mais chamados abertos usando `Counter` e `most_common(3)`
- [x] Retornar dicionário com: nome da empresa, chamados por status, total de chamados, quantidade em atraso, técnicos disponíveis e top 3 clientes

---

## Antes de passar para a Pessoa C

- [x] Rodar `python helpdesk_TRIO_NOMES.py` e confirmar que o bloco `__main__` executa sem erros
- [x] Confirmar que `resolver_chamado` lança `PermissionError` quando o técnico não é o responsável
- [x] Confirmar que `atribuicao_automatica()` retorna um `int`
- [x] Confirmar que `listar_em_atraso()` retorna lista de objetos `Chamado` (não dicts)
- [x] Confirmar que `painel_operacional()` retorna um dicionário com as chaves: `empresa`, `chamados_por_status`, `total_chamados`, `em_atraso`, `tecnicos_disponiveis`, `top3_clientes`
- [x] Confirmar que `abrir_chamado()` e `registrar_tecnico()` retornam os objetos criados
- [x] Passar o arquivo para a Pessoa C