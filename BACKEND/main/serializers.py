from rest_framework import serializers
from .models import CustomUser, Categoria, Livro, Emprestimo, itemEmprestimo

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'nome', 'cpf', 'grupo', 'foto', 'descricao', 'qtdLivros', 'groups', 'user_permissions']
        many = True

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        many = True

class LivroSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Livro
        fields = '__all__'
        many = True

class EmprestimoSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Emprestimo
        fields = '__all__'
        many = True

class itemEmprestimoSerializer(serializers.ModelSerializer): 

    class Meta:
        model = itemEmprestimo
        fields = '__all__'
        many = True