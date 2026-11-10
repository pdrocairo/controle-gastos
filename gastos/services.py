from decimal import Decimal

from .models import Ciclo, Conta, Gasto, GastoFixo
from datetime import date, timedelta

class CicloService:
    def ciclo_atual(data):
        ciclos = Ciclo.objects.all()
        
        for ciclo in ciclos:
            if data >= ciclo.data_inicio and data <= ciclo.data_fechamento:
                return ciclo
        return None

    def proximo_mes(mes: date) -> date:
        novo_mes = mes.month + 1
        novo_ano = mes.year

        if novo_mes >= 13:
            novo_mes = 1
            novo_ano = novo_ano + 1

        return mes.replace(day=1, month=novo_mes, year=novo_ano)

    def calcular_fechamento(conta: Conta, mes: date):
        dia_vencimento = conta.dia_vencimento_fatura
        proximo_mes = CicloService.proximo_mes(mes).replace(day=dia_vencimento)
        data_fechamento = proximo_mes - timedelta(days=7)
        return data_fechamento
    
    def criar_proximo_ciclo(ciclo: Ciclo):
        dia = ciclo.conta.dia_vencimento_fatura
        mes_referencia = CicloService.proximo_mes(ciclo.mes_referencia)
        data_inicio = mes_referencia.replace(day=dia)
        data_fechamento = CicloService.calcular_fechamento(ciclo.conta, mes_referencia)
        saldo = PainelService(ciclo, ciclo.data_fechamento).sobra()

        novo_ciclo = Ciclo.objects.create(conta=ciclo.conta, mes_referencia=mes_referencia, data_inicio=data_inicio, data_fechamento=data_fechamento, saldo_inicial=saldo)

        return novo_ciclo

    def garantir_proximo_ciclo(conta, hoje):
        pass

    def ciclo_do_gasto(conta: Conta, data: date):
        pass

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
        pass

    def sobra(self):
        gastos = self.ciclo.saldo_inicial - self.total_gastos()
        return gastos
        
    def dias_ate_fechamento(self):
        pass

    def gasto_por_dia(self):
        pass

    def estourou(self):
        pass
