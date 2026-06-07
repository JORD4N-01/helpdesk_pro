# Pessoa C — API Flask

**Arquivo:** `app.py`
**Aguardar a Pessoa B terminar e passar o arquivo antes de começar**

---

## Antes de começar

- [ ] Receber o arquivo `helpdesk_TRIO_NOMES.py` da Pessoa B
- [ ] Rodar `python helpdesk_TRIO_NOMES.py` e confirmar que executa sem erros
- [ ] Instalar Flask se necessário: `pip install flask`
- [ ] Criar o arquivo `app.py` na mesma pasta que `helpdesk_TRIO_NOMES.py`
- [ ] Confirmar com a Pessoa B quais exceções cada método pode lançar e qual código HTTP cada uma representa

---

## Bloco 1 — Configuração inicial do `app.py`

- [ ] Importar `Flask`, `request` e `jsonify` do flask
- [ ] Importar `CentralDeSupporte` do arquivo da Pessoa A/B
- [ ] Importar as três exceções customizadas: `ChamadoNaoEncontradoException`, `CapacidadeExcedidaException`, `TransicaoInvalidaException`
- [ ] Criar a instância `app = Flask(__name__)`
- [ ] Criar a instância `central = CentralDeSupporte("Ciesa Solutions")` **fora de qualquer rota** para o estado persistir entre requisições
- [ ] Adicionar o bloco `if __name__ == '__main__': app.run(debug=True, port=5000)` no final do arquivo

---

## Bloco 2 — Endpoints de chamados

### `POST /chamados`
- [ ] Ler `titulo`, `descricao`, `cliente` e `prioridade` do body com `request.get_json()`
- [ ] Chamar `central.abrir_chamado()` com os dados recebidos
- [ ] Retornar o chamado serializado com `to_dict()` e status HTTP `201`
- [ ] Capturar `ValueError` (prioridade inválida) e retornar `{'erro': ...}` com HTTP `400`
- [ ] Capturar `KeyError` (campo ausente no body) e retornar `{'erro': ...}` com HTTP `400`

### `GET /chamados`
- [ ] Ler o query param opcional `status` com `request.args.get('status')`
- [ ] Listar todos os chamados do dicionário `central.chamados`
- [ ] Se o param `status` foi informado, filtrar apenas os chamados com aquele status
- [ ] Retornar a lista serializada com `to_dict()` em cada chamado e HTTP `200`

### `GET /chamados/em-atraso`
- [ ] **Declarar esta rota antes de `GET /chamados/<int:numero>` no arquivo** — senão o Flask tenta converter `em-atraso` como inteiro e retorna erro
- [ ] Chamar `central.listar_em_atraso()`
- [ ] Retornar a lista serializada com `to_dict()` e HTTP `200`

### `GET /chamados/<int:numero>`
- [ ] Chamar `central.buscar_chamado(numero)`
- [ ] Retornar o chamado com `to_dict()` e HTTP `200`
- [ ] Capturar `ChamadoNaoEncontradoException` e retornar `{'erro': ...}` com HTTP `404`

### `PATCH /chamados/<int:numero>/status`
- [ ] Ler `novo_status` e `responsavel` do body
- [ ] Buscar o chamado e chamar `chamado.alterar_status(novo_status, responsavel)`
- [ ] Retornar o chamado atualizado com HTTP `200`
- [ ] Capturar `ChamadoNaoEncontradoException` → HTTP `404`
- [ ] Capturar `TransicaoInvalidaException` → HTTP `400`
- [ ] Capturar `KeyError` (campo ausente) → HTTP `400`

### `PATCH /chamados/<int:numero>/resolver`
- [ ] Ler `id_tecnico` e `descricao_solucao` do body
- [ ] Chamar `central.resolver_chamado(numero, id_tecnico, descricao_solucao)`
- [ ] Buscar o chamado novamente e retornar com `to_dict()` e HTTP `200`
- [ ] Capturar `ChamadoNaoEncontradoException` → HTTP `404`
- [ ] Capturar `PermissionError` (técnico não é o responsável) → HTTP `403`
- [ ] Capturar `TransicaoInvalidaException` ou `ValueError` → HTTP `400`
- [ ] Capturar `KeyError` (campo ausente) → HTTP `400`

---

## Bloco 3 — Endpoints de técnicos

### `POST /tecnicos`
- [ ] Ler `nome`, `especialidades` e opcionalmente `capacidade_maxima` do body
- [ ] Usar `dados.get('capacidade_maxima', 5)` para o valor padrão quando não informado
- [ ] Chamar `central.registrar_tecnico()` com os dados
- [ ] Retornar o técnico serializado com `to_dict()` e HTTP `201`
- [ ] Capturar `KeyError` (campo ausente) → HTTP `400`

### `GET /tecnicos`
- [ ] Ler o query param opcional `disponivel` com `request.args.get('disponivel')`
- [ ] Listar todos os técnicos do dicionário `central.tecnicos`
- [ ] Se `disponivel=true`, filtrar apenas os com `tecnico.disponivel == True`
- [ ] Se `disponivel=false`, filtrar apenas os com `tecnico.disponivel == False`
- [ ] Retornar a lista serializada com `to_dict()` e HTTP `200`

---

## Bloco 4 — Atribuição automática e painel

### `POST /atribuicao/automatica`
- [ ] Chamar `central.atribuicao_automatica()` e guardar a quantidade retornada
- [ ] Montar a lista dos chamados atualmente em status `'em_atendimento'`
- [ ] Retornar dicionário com `atribuidos` (quantidade) e `chamados` (lista serializada) e HTTP `200`

### `GET /painel`
- [ ] Chamar `central.painel_operacional()`
- [ ] Retornar o resultado diretamente com `jsonify()` e HTTP `200`

---

## Bloco 5 — Revisão geral antes de testar

- [ ] Confirmar que toda rota retorna `jsonify()` — nunca strings ou dicionários puros
- [ ] Confirmar que todo erro retorna `{'erro': str(e)}` com o código HTTP adequado
- [ ] Confirmar que a rota `GET /chamados/em-atraso` está declarada antes de `GET /chamados/<int:numero>`
- [ ] Confirmar que `central` é instanciada fora de qualquer função de rota
- [ ] Rodar `python app.py` e verificar que o servidor sobe sem erros na porta 5000

---

## Bloco 6 — Testes no Postman

Execute na ordem abaixo — cada etapa depende das anteriores.

- [ ] Criar uma Collection chamada `HelpDesk Pro` no Postman
- [ ] Criar uma Environment com a variável `base_url = http://localhost:5000`
- [ ] Usar `{{base_url}}` em todas as URLs das requisições

### Sequência de testes

- [ ] `POST /tecnicos` × 4 — verificar que cada um retorna `201` e `id_tecnico` sequencial (1, 2, 3, 4)
- [ ] `POST /chamados` × 8 — verificar que cada um retorna `201`, `numero` sequencial e `sla_horas` calculado automaticamente
- [ ] `POST /atribuicao/automatica` — verificar balanceamento: com 8 chamados e 4 técnicos deve distribuir 2 por técnico
- [ ] `GET /chamados` — verificar que retorna todos os 8 chamados
- [ ] `GET /chamados?status=em_atendimento` — verificar que filtra corretamente
- [ ] `GET /chamados/1` — verificar retorno `200` com dados completos
- [ ] `GET /chamados/999` — verificar retorno `404` com campo `erro`
- [ ] `PATCH /chamados/1/status` com `novo_status: aguardando_cliente` — verificar `200`
- [ ] `PATCH /chamados/1/status` com `novo_status: fechado` — verificar `400` (transição inválida)
- [ ] `PATCH /chamados/1/resolver` com o técnico correto — verificar `200`
- [ ] `PATCH /chamados/2/resolver` com um técnico que não é o responsável — verificar `403`
- [ ] `PATCH /chamados/1/status` com `novo_status: fechado` após resolver — verificar `200`
- [ ] `GET /tecnicos?disponivel=true` — verificar que lista apenas os com vaga
- [ ] `GET /tecnicos?disponivel=false` — verificar que lista apenas os lotados
- [ ] `GET /chamados/em-atraso` — verificar lista ordenada do mais atrasado ao mais recente
- [ ] `GET /painel` — verificar que o retorno contém: `chamados_por_status`, `em_atraso`, `tecnicos_disponiveis`, `top3_clientes`

---

## Entrega final do trio

- [ ] Confirmar que os dois arquivos estão na mesma pasta: `helpdesk_TRIO_NOMES.py` e `app.py`
- [ ] Rodar `python helpdesk_TRIO_NOMES.py` — bloco `__main__` deve executar sem erros
- [ ] Rodar `python app.py` — servidor deve subir sem erros
- [ ] Executar todos os testes do Postman na sequência e confirmar que todos passam
- [ ] Verificar que o nome do arquivo contém os nomes reais dos três integrantes