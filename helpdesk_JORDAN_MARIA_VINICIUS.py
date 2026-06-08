from datetime import datetime, timedelta
from collections import deque, Counter


class ChamadoNaoEncontradoException(Exception):
    pass


class CapacidadeExcedidaException(Exception):
    pass


class TransicaoInvalidaException(Exception):
    pass


class Chamado:
    _contador = 0
    SLA_MAP = {
        'critica': 4,
        'alta': 8,
        'media': 24,
        'baixa': 72,
    }
    TRANSICOES = {
        'aberto': {'em_atendimento'},
        'em_atendimento': {'resolvido', 'aguardando_cliente'},
        'aguardando_cliente': {'em_atendimento'},
        'resolvido': {'fechado'},
        'fechado': set(),
    }

    def __init__(self, titulo, descricao, cliente, prioridade):
        if prioridade not in self.SLA_MAP:
            raise ValueError(f"Prioridade invalida: {prioridade}. Opcoes: {', '.join(self.SLA_MAP.keys())}")

        type(self)._contador += 1
        self.numero = type(self)._contador
        self.titulo = titulo
        self.descricao = descricao
        self.cliente = cliente
        self.prioridade = prioridade
        self.status = 'aberto'
        self.data_abertura = datetime.now()
        self.sla_horas = self.SLA_MAP[prioridade]
        self.tecnico = None
        self.historico = []

    def __str__(self):
        return f"#{self.numero} - {self.titulo} ({self.cliente}) | Prioridade: {self.prioridade} | Status: {self.status} | Tempo decorrido: {self.tempo_decorrido()}"

    def tempo_decorrido(self):
        return datetime.now() - self.data_abertura

    def esta_em_atraso(self):
        if self.status in ('resolvido', 'fechado'):
            return False
        horas_passadas = self.tempo_decorrido().total_seconds() / 3600
        return horas_passadas > self.sla_horas

    def registrar_acao(self, acao, responsavel):
        self.historico.append({
            'data': datetime.now().isoformat(),
            'acao': acao,
            'responsavel': responsavel,
        })

    def alterar_status(self, novo_status, responsavel='sistema'):
        permitidos = self.TRANSICOES.get(self.status, set())
        if novo_status not in permitidos:
            raise TransicaoInvalidaException(
                f"Transicao invalida: {self.status} -> {novo_status}. "
                f"Transicoes permitidas: {', '.join(permitidos) if permitidos else 'nenhuma'}"
            )
        self.status = novo_status
        self.registrar_acao(f"Status alterado para {novo_status}", responsavel)

    def to_dict(self):
        return {
            'numero': self.numero,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'cliente': self.cliente,
            'prioridade': self.prioridade,
            'status': self.status,
            'data_abertura': self.data_abertura.isoformat(),
            'sla_horas': self.sla_horas,
            'tecnico': self.tecnico,
            'historico': self.historico,
            'em_atraso': self.esta_em_atraso(),
        }


class Tecnico:
    _contador = 0

    def __init__(self, nome, especialidades, capacidade_maxima=5):
        type(self)._contador += 1
        self.id_tecnico = type(self)._contador
        self.nome = nome
        self.especialidades = set(especialidades) if not isinstance(especialidades, set) else especialidades
        self.capacidade_maxima = capacidade_maxima
        self.chamados_ativos = []
        self.disponivel = True

    def __str__(self):
        return f"#{self.id_tecnico} - {self.nome} | Especialidades: {', '.join(self.especialidades)} | Chamados ativos: {len(self.chamados_ativos)} | Disponivel: {'Sim' if self.disponivel else 'Nao'}"

    def atribuir_chamado(self, numero):
        if not self.disponivel:
            raise CapacidadeExcedidaException(f"Tecnico {self.nome} (#{self.id_tecnico}) ja atingiu a capacidade maxima de {self.capacidade_maxima} chamados")
        self.chamados_ativos.append(numero)
        self.disponivel = len(self.chamados_ativos) < self.capacidade_maxima

    def liberar_chamado(self, numero):
        if numero not in self.chamados_ativos:
            raise ValueError(f"Chamado #{numero} nao esta atribuido ao tecnico {self.nome} (#{self.id_tecnico})")
        self.chamados_ativos.remove(numero)
        self.disponivel = len(self.chamados_ativos) < self.capacidade_maxima

    def tem_especialidade(self, categoria):
        return categoria in self.especialidades

    def to_dict(self):
        return {
            'id_tecnico': self.id_tecnico,
            'nome': self.nome,
            'especialidades': list(self.especialidades),
            'capacidade_maxima': self.capacidade_maxima,
            'chamados_ativos': self.chamados_ativos,
            'disponivel': self.disponivel,
        }


class CentralDeSupporte:
    def __init__(self, empresa):
        self.empresa = empresa
        self.chamados = {}
        self.tecnicos = {}
        self.fila_nao_atribuidos = deque()

    def abrir_chamado(self, titulo, descricao, cliente, prioridade):
        chamado = Chamado(titulo, descricao, cliente, prioridade)
        self.chamados[chamado.numero] = chamado
        self.fila_nao_atribuidos.append(chamado.numero)
        return chamado

    def registrar_tecnico(self, nome, especialidades, capacidade_maxima=5):
        tecnico = Tecnico(nome, especialidades, capacidade_maxima)
        self.tecnicos[tecnico.id_tecnico] = tecnico
        return tecnico

    def buscar_chamado(self, numero):
        if numero not in self.chamados:
            raise ChamadoNaoEncontradoException(f"Chamado #{numero} nao encontrado")
        return self.chamados[numero]

    def atribuir_tecnico(self, numero, id_tecnico):
        chamado = self.buscar_chamado(numero)

        if id_tecnico not in self.tecnicos:
            raise ChamadoNaoEncontradoException(f"Tecnico #{id_tecnico} nao encontrado")

        tecnico = self.tecnicos[id_tecnico]
        tecnico.atribuir_chamado(numero)
        chamado.tecnico = id_tecnico
        chamado.alterar_status('em_atendimento', tecnico.nome)
        chamado.registrar_acao(f"Chamado atribuido ao tecnico {tecnico.nome}", tecnico.nome)

        if numero in self.fila_nao_atribuidos:
            self.fila_nao_atribuidos.remove(numero)

    def atribuicao_automatica(self):
        nao_atribuidos = deque()
        atribuidos = 0

        while self.fila_nao_atribuidos:
            numero = self.fila_nao_atribuidos.popleft()
            chamado = self.chamados[numero]

            disponiveis = [t for t in self.tecnicos.values() if t.disponivel]

            if not disponiveis:
                nao_atribuidos.append(numero)
                continue

            tecnico = min(disponiveis, key=lambda t: (len(t.chamados_ativos), t.id_tecnico))

            tecnico.atribuir_chamado(numero)
            chamado.tecnico = tecnico.id_tecnico
            chamado.alterar_status('em_atendimento', 'sistema')
            chamado.registrar_acao(f"Chamado atribuido ao tecnico {tecnico.nome} (atribuicao automatica)", 'sistema')
            atribuidos += 1

        self.fila_nao_atribuidos = nao_atribuidos
        return atribuidos

    def resolver_chamado(self, numero, id_tecnico, descricao_solucao):
        chamado = self.buscar_chamado(numero)

        if chamado.tecnico != id_tecnico:
            raise PermissionError(f"Chamado #{numero} nao esta atribuido ao tecnico #{id_tecnico}")

        tecnico = self.tecnicos[id_tecnico]
        chamado.alterar_status('resolvido', tecnico.nome)
        chamado.registrar_acao(f"Solucao: {descricao_solucao}", tecnico.nome)
        tecnico.liberar_chamado(numero)

    def fechar_chamado(self, numero):
        chamado = self.buscar_chamado(numero)
        chamado.alterar_status('fechado', 'sistema')

    def listar_em_atraso(self):
        atrasados = [c for c in self.chamados.values() if c.esta_em_atraso()]
        atrasados.sort(key=lambda c: c.tempo_decorrido(), reverse=True)
        return atrasados

    def relatorio_por_prioridade(self):
        relatorio = {p: [] for p in Chamado.SLA_MAP.keys()}
        for chamado in self.chamados.values():
            if chamado.status not in ('resolvido', 'fechado'):
                relatorio[chamado.prioridade].append(chamado.to_dict())
        return relatorio

    def painel_operacional(self):
        status_counts = Counter(c.status for c in self.chamados.values())

        em_atraso = self.listar_em_atraso()

        tecnicos_disponiveis = [t.to_dict() for t in self.tecnicos.values() if t.disponivel]

        clientes_abertos = [c.cliente for c in self.chamados.values() if c.status not in ('resolvido', 'fechado')]
        top3 = Counter(clientes_abertos).most_common(3)

        return {
            'empresa': self.empresa,
            'chamados_por_status': dict(status_counts),
            'total_chamados': len(self.chamados),
            'em_atraso': len(em_atraso),
            'tecnicos_disponiveis': tecnicos_disponiveis,
            'top3_clientes': [{'cliente': c, 'quantidade': q} for c, q in top3],
        }


if __name__ == '__main__':
    central = CentralDeSupporte("Ciesa Solutions")

    central.registrar_tecnico("Jordan", {"redes", "hardware"}, 3)
    central.registrar_tecnico("Maria", {"software", "banco_dados"}, 3)
    central.registrar_tecnico("Vinicius", {"redes", "seguranca"}, 3)
    central.registrar_tecnico("David", {"hardware", "software"}, 3)

    central.abrir_chamado("PC nao liga", "Fonte queimada", "Empresa X", "critica")
    central.abrir_chamado("Internet lenta", "Queda de pacotes", "Empresa Y", "alta")
    central.abrir_chamado("Sistema trava", "Erro ao salvar", "Empresa Z", "media")
    central.abrir_chamado("Virus detectado", "Antivirus bloqueou", "Empresa X", "critica")
    central.abrir_chamado("Impressora parou", "Driver corrompido", "Empresa W", "baixa")
    central.abrir_chamado("Email nao envia", "Configuracao SMTP", "Empresa Y", "alta")
    central.abrir_chamado("Backup falhou", "Disco cheio", "Empresa Z", "media")
    central.abrir_chamado("Acesso negado", "Permissao incorreta", "Empresa W", "baixa")

    atribuidos = central.atribuicao_automatica()
    print(f"Chamados atribuidos automaticamente: {atribuidos}")

    central.resolver_chamado(1, 1, "Substituida fonte de alimentacao")
    central.resolver_chamado(2, 2, "Reconfigurado roteador e otimizado sinal")

    central.fechar_chamado(1)

    try:
        central.buscar_chamado(1).alterar_status('fechado', 'sistema')
    except TransicaoInvalidaException as e:
        print(f"Transicao invalida capturada: {e}")

    from datetime import timedelta
    chamado_atrasado = central.buscar_chamado(3)
    chamado_atrasado.data_abertura -= timedelta(hours=48)

    print("\nChamados em atraso:")
    for chamado in central.listar_em_atraso():
        print(f"  #{chamado.numero} - {chamado.titulo} ({chamado.cliente})")

    print("\nPainel operacional:")
    from pprint import pprint
    pprint(central.painel_operacional())
