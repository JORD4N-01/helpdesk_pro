# Pessoa B — Lógica de Negócio

**Arquivo:** `helpdesk_TRIO_NOMES.py` (mesmo arquivo da Pessoa A)
**Aguardar a Pessoa A terminar e passar o arquivo antes de começar**

---

## Antes de começar

- [ ] Receber o arquivo da Pessoa A e verificar que ele roda sem erros com `python helpdesk_TRIO_NOMES.py`
- [ ] Confirmar com a Pessoa A os nomes exatos das exceções, atributos e o que `to_dict()` retorna
- [ ] Verificar que `from collections import deque` já está nos imports, adicionar se não estiver
- [ ] Adicionar `from collections import Counter` nos imports

---

## Bloco 1 — Estrutura da `CentralDeSupporte`

### Método `__init__`
- [ ] Receber `empresa` como parâmetro e salvar no atributo
- [ ] Criar `self.chamados` como `dict` vazio — justificativa: hash table garante busca O(1) mesmo com milhares de registros, requisito crítico do projeto
- [ ] Criar `self.tecnicos` como `dict` vazio
- [ ] Criar `self.fila_nao_atribuidos` como `deque()` vazia — justificativa: `popleft()` é O(1), enquanto `list.pop(0)` seria O(n)

### Método `abrir_chamado`
- [ ] Criar um objeto `Chamado` com os parâmetros recebidos
- [ ] Armazenar o chamado em `self.chamados` usando o número do chamado como chave
- [ ] Adicionar o número à `fila_nao_atribuidos` com `append`
- [ ] Retornar o objeto criado

### Método `registrar_tecnico`
- [ ] Criar um objeto `Tecnico` com os parâmetros recebidos
- [ ] Armazenar em `self.tecnicos` usando o `id_tecnico` como chave
- [ ] Retornar o objeto criado

---

## Bloco 2 — Busca

### Método `buscar_chamado`
- [ ] Tentar recuperar o chamado do dicionário `self.chamados` pelo número
- [ ] Lançar `ChamadoNaoEncontradoException` com mensagem clara se o número não existir
- [ ] Retornar o objeto `Chamado` encontrado
- [ ] **Atenção:** este é o método que justifica o uso de `dict` — o professor vai perguntar sobre ele

---

## Bloco 3 — Atribuição manual

### Método `atribuir_tecnico`
- [ ] Buscar o chamado pelo número usando `buscar_chamado()` (já trata o 404)
- [ ] Verificar se o `id_tecnico` existe em `self.tecnicos`, lançar `ChamadoNaoEncontradoException` se não existir
- [ ] Chamar `tecnico.atribuir_chamado(numero)` — o método da Pessoa A já lança `CapacidadeExcedidaException` se necessário
- [ ] Atribuir o `id_tecnico` ao atributo `chamado.tecnico`
- [ ] Chamar `chamado.alterar_status('em_atendimento', nome_do_tecnico)`
- [ ] Registrar no histórico que o chamado foi atribuído ao técnico
- [ ] Remover o número da `fila_nao_atribuidos` se ainda estiver nela

---

## Bloco 4 — Atribuição automática

### Método `atribuicao_automatica`
- [ ] Criar uma deque auxiliar para chamados que não puderam ser atribuídos
- [ ] Percorrer a fila com `popleft()` enquanto houver itens
- [ ] Para cada chamado, filtrar apenas os técnicos com `disponivel == True`
- [ ] Se não houver técnico disponível, recolocar o chamado na deque auxiliar e continuar
- [ ] Selecionar o técnico com menor quantidade de chamados ativos — em caso de empate, escolher o de menor `id_tecnico`
- [ ] Realizar a atribuição: chamar `atribuir_chamado`, atualizar `chamado.tecnico`, mudar status para `'em_atendimento'` e registrar no histórico como ação do sistema
- [ ] Incrementar um contador a cada atribuição realizada
- [ ] Ao final, substituir `fila_nao_atribuidos` pela deque auxiliar com os não atribuídos
- [ ] Retornar o contador com a quantidade total de chamados atribuídos

---

## Bloco 5 — Resolução e fechamento

### Método `resolver_chamado`
- [ ] Buscar o chamado pelo número usando `buscar_chamado()`
- [ ] Verificar se `chamado.tecnico` é igual ao `id_tecnico` recebido
- [ ] Lançar `PermissionError` com mensagem clara se o técnico não for o responsável — **a Pessoa C usa esta exceção para retornar HTTP 403**
- [ ] Chamar `chamado.alterar_status('resolvido', nome_do_tecnico)`
- [ ] Registrar a descrição da solução no histórico do chamado
- [ ] Chamar `tecnico.liberar_chamado(numero)` para liberar o técnico

### Método `fechar_chamado`
- [ ] Buscar o chamado pelo número usando `buscar_chamado()`
- [ ] Chamar `chamado.alterar_status('fechado', 'sistema')` — a validação de transição já está no `alterar_status` da Pessoa A

---

## Bloco 6 — Relatórios

### Método `listar_em_atraso`
- [ ] Filtrar todos os chamados do dicionário onde `esta_em_atraso()` retorna `True`
- [ ] Ordenar a lista pelo tempo decorrido de forma decrescente (mais atrasado primeiro)
- [ ] Retornar a lista ordenada de objetos `Chamado`

### Método `relatorio_por_prioridade`
- [ ] Criar um dicionário com as quatro chaves de prioridade como listas vazias
- [ ] Percorrer os chamados e agrupar os que não estão resolvidos nem fechados pela prioridade
- [ ] Retornar o dicionário com listas de chamados serializados com `to_dict()`

### Método `painel_operacional`
- [ ] Contar quantos chamados existem em cada status usando `Counter`
- [ ] Obter a quantidade de chamados em atraso chamando `listar_em_atraso()`
- [ ] Listar os técnicos disponíveis serializados com `to_dict()`
- [ ] Identificar os 3 clientes com mais chamados abertos usando `Counter` e `most_common(3)`
- [ ] Retornar dicionário com: nome da empresa, chamados por status, total de chamados, quantidade em atraso, técnicos disponíveis e top 3 clientes

---

## Antes de passar para a Pessoa C

- [ ] Rodar `python helpdesk_TRIO_NOMES.py` e confirmar que o bloco `__main__` executa sem erros
- [ ] Confirmar que `resolver_chamado` lança `PermissionError` quando o técnico não é o responsável
- [ ] Confirmar que `atribuicao_automatica()` retorna um `int`
- [ ] Confirmar que `listar_em_atraso()` retorna lista de objetos `Chamado` (não dicts)
- [ ] Confirmar que `painel_operacional()` retorna um dicionário com as chaves: `empresa`, `chamados_por_status`, `total_chamados`, `em_atraso`, `tecnicos_disponiveis`, `top3_clientes`
- [ ] Confirmar que `abrir_chamado()` e `registrar_tecnico()` retornam os objetos criados
- [ ] Passar o arquivo para a Pessoa C