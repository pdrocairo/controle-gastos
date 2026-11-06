from django.contrib import admin
from .models import Categoria, Gasto, GastoFixo, Ciclo, Conta

admin.site.register(Categoria)
admin.site.register(Gasto)
admin.site.register(GastoFixo)
admin.site.register(Ciclo)
admin.site.register(Conta)