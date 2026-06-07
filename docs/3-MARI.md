# Pessoa C — API Flask

**Arquivo:** `app.py`
**Aguardar a Pessoa B terminar e passar o arquivo antes de começar**

---

## Antes de começar

- [x] Receber o arquivo `helpdesk_TRIO_NOMES.py` da Pessoa B
- [x] Rodar `python helpdesk_TRIO_NOMES.py` e confirmar que executa sem erros
- [x] Instalar Flask se necessário: `pip install flask`
- [x] Criar o arquivo `app.py` na mesma pasta que `helpdesk_TRIO_NOMES.py`
- [x] Confirmar com a Pessoa B quais exceções cada método pode lançar e qual código HTTP cada uma representa

---

## Bloco 1 — Configuração inicial do `app.py`

- [x] Importar `Flask`, `request` e `jsonify` do flask
- [x] Importar `CentralDeSupporte` do arquivo da Pessoa A/B
- [x] Importar as três exceções customizadas: `ChamadoNaoEncontradoException`, `CapacidadeExcedidaException`, `TransicaoInvalidaException`
- [x] Criar a instância `app = Flask(__name__)`
- [x] Criar a instância `central = CentralDeSupporte("Ciesa Solutions")` **fora de qualquer rota** para o estado persistir entre requisições
- [x] Adicionar o bloco `if __name__ == '__main__': app.run(debug=True, port=5000)` no final do arquivo

---

## Bloco 2 — Endpoints de chamados

### `POST /chamados`
- [x] Ler `titulo`, `descricao`, `cliente` e `prioridade` do body com `request.get_json()`
- [x] Chamar `central.abrir_chamado()` com os dados recebidos
- [x] Retornar o chamado serializado com `to_dict()` e status HTTP `201`
- [x] Capturar `ValueError` (prioridade inválida) e retornar `{'erro': ...}` com HTTP `400`
- [x] Capturar `KeyError` (campo ausente no body) e retornar `{'erro': ...}` com HTTP `400`

### `GET /chamados`
- [x] Ler o query param opcional `status` com `request.args.get('status')`
- [x] Listar todos os chamados do dicionário `central.chamados`
- [x] Se o param `status` foi informado, filtrar apenas os chamados com aquele status
- [x] Retornar a lista serializada com `to_dict()` em cada chamado e HTTP `200`

### `GET /chamados/em-atraso`
- [x] **Declarar esta rota antes de `GET /chamados/<int:numero>` no arquivo** — senão o Flask tenta converter `em-atraso` como inteiro e retorna erro
- [x] Chamar `central.listar_em_atraso()`
- [x] Retornar a lista serializada com `to_dict()` e HTTP `200`

### `GET /chamados/<int:numero>`
- [x] Chamar `central.buscar_chamado(numero)`
- [x] Retornar o chamado com `to_dict()` e HTTP `200`
- [x] Capturar `ChamadoNaoEncontradoException` e retornar `{'erro': ...}` com HTTP `404`

### `PATCH /chamados/<int:numero>/status`
- [x] Ler `novo_status` e `responsavel` do body
- [x] Buscar o chamado e chamar `chamado.alterar_status(novo_status, responsavel)`
- [x] Retornar o chamado atualizado com HTTP `200`
- [x] Capturar `ChamadoNaoEncontradoException` → HTTP `404`
- [x] Capturar `TransicaoInvalidaException` → HTTP `400`
- [x] Capturar `KeyError` (campo ausente) → HTTP `400`

### `PATCH /chamados/<int:numero>/resolver`
- [x] Ler `id_tecnico` e `descricao_solucao` do body
- [x] Chamar `central.resolver_chamado(numero, id_tecnico, descricao_solucao)`
- [x] Buscar o chamado novamente e retornar com `to_dict()` e HTTP `200`
- [x] Capturar `ChamadoNaoEncontradoException` → HTTP `404`
- [x] Capturar `PermissionError` (técnico não é o responsável) → HTTP `403`
- [x] Capturar `TransicaoInvalidaException` ou `ValueError` → HTTP `400`
- [x] Capturar `KeyError` (campo ausente) → HTTP `400`

---

## Bloco 3 — Endpoints de técnicos

### `POST /tecnicos`
- [x] Ler `nome`, `especialidades` e opcionalmente `capacidade_maxima` do body
- [x] Usar `dados.get('capacidade_maxima', 5)` para o valor padrão quando não informado
- [x] Chamar `central.registrar_tecnico()` com os dados
- [x] Retornar o técnico serializado com `to_dict()` e HTTP `201`
- [x] Capturar `KeyError` (campo ausente) → HTTP `400`

### `GET /tecnicos`
- [x] Ler o query param opcional `disponivel` com `request.args.get('disponivel')`
- [x] Listar todos os técnicos do dicionário `central.tecnicos`
- [x] Se `disponivel=true`, filtrar apenas os com `tecnico.disponivel == True`
- [x] Se `disponivel=false`, filtrar apenas os com `tecnico.disponivel == False`
- [x] Retornar a lista serializada com `to_dict()` e HTTP `200`

---

## Bloco 4 — Atribuição automática e painel

### `POST /atribuicao/automatica`
- [x] Chamar `central.atribuicao_automatica()` e guardar a quantidade retornada
- [x] Montar a lista dos chamados atualmente em status `'em_atendimento'`
- [x] Retornar dicionário com `atribuidos` (quantidade) e `chamados` (lista serializada) e HTTP `200`

### `GET /painel`
- [x] Chamar `central.painel_operacional()`
- [x] Retornar o resultado diretamente com `jsonify()` e HTTP `200`

---

## Bloco 5 — Revisão geral antes de testar

- [x] Confirmar que toda rota retorna `jsonify()` — nunca strings ou dicionários puros
- [x] Confirmar que todo erro retorna `{'erro': str(e)}` com o código HTTP adequado
- [x] Confirmar que a rota `GET /chamados/em-atraso` está declarada antes de `GET /chamados/<int:numero>`
- [x] Confirmar que `central` é instanciada fora de qualquer função de rota
- [x] Rodar `python app.py` e verificar que o servidor sobe sem erros na porta 5000

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

- [x] Confirmar que os dois arquivos estão na mesma pasta: `helpdesk_TRIO_NOMES.py` e `app.py`
- [x] Rodar `python helpdesk_TRIO_NOMES.py` — bloco `__main__` deve executar sem erros
- [x] Rodar `python app.py` — servidor deve subir sem erros
- [ ] Executar todos os testes do Postman na sequência e confirmar que todos passam — *manual*
- [x] Verificar que o nome do arquivo contém os nomes reais dos três integrantes