from decimal import Decimal

from .models import Ciclo, Conta, Gasto, GastoFixo
from datetime import date, timedelta

class CicloService:
    @staticmethod
    def ciclo_da_data(conta: Conta, data: date) -> Ciclo | None:
        return Ciclo.objects.filter(conta=conta, data_inicio__lte=data, data_fechamento__gt=data).first()

    @staticmethod
    def proximo_mes(mes: date) -> date:
        novo_mes = mes.month + 1
        novo_ano = mes.year

        if novo_mes >= 13:
            novo_mes = 1
            novo_ano = novo_ano + 1

        return mes.replace(day=1, month=novo_mes, year=novo_ano)

    @staticmethod
    def calcular_fechamento(conta: Conta, mes: date):
        dia_vencimento = conta.dia_vencimento_fatura
        vencimento = CicloService.proximo_mes(mes).replace(day=dia_vencimento)
        data_fechamento = vencimento - timedelta(days=7)
        return data_fechamento

    @staticmethod
    def criar_proximo_ciclo(ciclo: Ciclo):
        mes_referencia = CicloService.proximo_mes(ciclo.mes_referencia)
        data_inicio = ciclo.data_fechamento
        data_fechamento = CicloService.calcular_fechamento(ciclo.conta, mes_referencia)
        saldo = PainelService(ciclo, ciclo.data_fechamento).pode_gastar()

        novo_ciclo = Ciclo.objects.create(conta=ciclo.conta, mes_referencia=mes_referencia, data_inicio=data_inicio, data_fechamento=data_fechamento, saldo_inicial=saldo)

        return novo_ciclo

    @staticmethod
    def garantir_proximo_ciclo(conta: Conta, hoje: date):
            ultimo_ciclo = Ciclo.objects.filter(conta=conta).order_by("-data_fechamento").first()
            if ultimo_ciclo is None:
                return None

            while hoje >= ultimo_ciclo.data_fechamento:
                ultimo_ciclo = CicloService.criar_proximo_ciclo(ultimo_ciclo)

            return ultimo_ciclo

class PainelService:
    def __init__(self, ciclo: Ciclo, hoje: date):
        self.ciclo = ciclo
        self.hoje = hoje

    def total_gastos(self):
        return self.total_gastos_variaveis() + self.total_fixos()

        
    def total_gastos_variaveis(self):
        gastos_variaveis = Gasto.objects.filter(ciclo=self.ciclo)

        gastos_total = Decimal("0")
        for gasto in gastos_variaveis:
            gastos_total = gastos_total +gasto.valor

        return gastos_total
    
    def total_fixos(self):
        gastos_fixos = GastoFixo.objects.filter(conta=self.ciclo.conta)

        total_gasto_fixo = Decimal("0")
        for gasto in gastos_fixos:
            total_gasto_fixo = total_gasto_fixo + gasto.valor

        return total_gasto_fixo


    def pode_gastar(self):
        saldo = self.ciclo.saldo_inicial - self.total_gastos()
        return saldo
        
    def dias_ate_fechamento(self):
        data_fechamento = self.ciclo.data_fechamento
        res = (data_fechamento - self.hoje).days
        if res > 0:
            return res
        return 0

    def gasto_por_dia(self):
        if self.estourou() or self.dias_ate_fechamento() == 0:
            return Decimal("0")
        return self.pode_gastar() / self.dias_ate_fechamento()
            

    def estourou(self):
        if self.pode_gastar() < 0:
            return True
        return False
