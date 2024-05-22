from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AdminUsuarioCustomizado(admin.ModelAdmin):
    model=CustomUser
    list_display = ['id', 'email', 'qtdLivros']
    list_display_links = ('id', 'email', 'qtdLivros',)  
    search_fields = ['email',] 

admin.site.register(CustomUser,AdminUsuarioCustomizado)

class AdminCategoria(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ('id', 'nome',)
    search_fields = ('nome',)
    list_per_page = 10

admin.site.register(Categoria,AdminCategoria)

class AdminLivro(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ('id', 'nome',)
    search_fields = ('id',)
    list_per_page = 10

admin.site.register(Livro,AdminLivro)

class AdminEmprestimo(admin.ModelAdmin):
    list_display = ['id', 'idUsuario']
    list_display_links = ('id', 'idUsuario',)
    search_fields = ('id',)
    list_per_page = 10

admin.site.register(Emprestimo,AdminEmprestimo)