from rest_framework import filters
import django_filters 

from .models import *

class CustomUserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    nome = django_filters.CharFilter(lookup_expr='icontains')
    cpf = django_filters.NumberFilter()
    grupo = django_filters.CharFilter(lookup_expr='exact')
    qtdLivros = django_filters.NumberFilter()
    
    class Meta:
        model = CustomUser
        fields = ['email', 'nome', 'cpf', 'grupo', 'qtdLivros']

class CategoriaFilter(django_filters.FilterSet):
   nome = django_filters.CharFilter(lookup_expr='icontains')

   class Meta:
      model = Categoria
      fields = ['nome']

class LivroFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    valor = django_filters.NumberFilter()
    idFormato = django_filters.CharFilter(lookup_expr='exact')
    idStatus = django_filters.CharFilter(lookup_expr='exact')
    idCategoria = django_filters.NumberFilter()

    class Meta:
        model = Livro
        fields = ['nome', 'valor', 'idFormato', 'idStatus', 'idCategoria']

class EmprestimoFilter(django_filters.FilterSet):
    idUsuario = django_filters.NumberFilter()
    dtRealizacao = django_filters.DateFilter()
    dtPrevisão = django_filters.DateFilter()
    dtDevolucao = django_filters.DateFilter()
    valorTotal = django_filters.NumberFilter()
    qtdLivros = django_filters.NumberFilter()
    situacao = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Emprestimo
        fields = ['idUsuario', 'dtRealizacao', 'dtPrevisão', 'dtDevolucao', 'valorTotal', 'qtdLivros', 'situacao']

class ItemEmprestimoFilter(django_filters.FilterSet):
    idEmprestimo = django_filters.NumberFilter()
    idLivro = django_filters.NumberFilter()

    class Meta:
        model = itemEmprestimo
        fields = ['idEmprestimo', 'idLivro']