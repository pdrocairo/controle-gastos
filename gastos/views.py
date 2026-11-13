from django.shortcuts import render
from django.http import Http404, HttpResponse
from .services import CicloService, PainelService,ContaService
from datetime import date
from django.contrib.auth.decorators import login_required


def home(request):
    return HttpResponse("oi")

@login_required
def exibir_painel(request):
    hoje = date.today()
    conta = ContaService.busca_conta()
    
    if conta is None:
        raise Http404("Nenhuma conta cadastrada")

    ciclo = CicloService.garantir_proximo_ciclo(conta, hoje)

    if ciclo is None:
        raise Http404("Nenhum ciclo cadastrado")

    painel = PainelService(ciclo, hoje)

    contexto = {
        "conta": conta, 
        "ciclo": ciclo,
        "saldo": painel.pode_gastar(),
        "gastos_por_dia": painel.gasto_por_dia(),
        "dias_restantes": painel.dias_ate_fechamento(),
        "gastos_fixos": painel.total_fixos(),
        "gastos_variaveis": painel.total_gastos_variaveis(),
        "estourou_orcamento": painel.estourou()
    }

    return render(request, "gastos/painel.html",context=contexto)