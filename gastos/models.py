from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=80)

class Conta(models.Model):
    nome = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    dia_vencimento_fatura = models.PositiveSmallIntegerField()

class Ciclo(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    mes_referencia = models.DateField()
    data_inicio = models.DateField()
    data_fechamento = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=10,decimal_places=2, default=0)

class Gasto(models.Model):
    ciclo = models.ForeignKey(Ciclo, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=150, blank=True)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    data =  models.DateField()

class GastoFixo(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=150, blank=True)
    valor = models.DecimalField(max_digits=10,decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField()



