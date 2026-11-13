from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome

class Conta(models.Model):
    nome = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    dia_vencimento_fatura = models.PositiveSmallIntegerField()
    dono = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.nome} {self.banco}"
    
class Ciclo(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    mes_referencia = models.DateField()
    data_inicio = models.DateField()
    data_fechamento = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=10,decimal_places=2, default=0)

    def __str__(self):
        return f"{self.conta.banco} {self.mes_referencia.strftime('%m/%Y')}"

class Gasto(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=150, blank=True)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    data =  models.DateField()

    def __str__(self):
        return f"{self.descricao} R${self.valor} {self.data.strftime('%d/%m/%Y')}"
    
class GastoFixo(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=150, blank=True)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.descricao or 'Sem descrição'} R${self.valor} dia:{self.dia_vencimento}"


