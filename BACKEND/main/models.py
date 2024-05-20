from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.admin.models import LogEntry
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .gerenciador import Gerenciador


GRUPOS = [
    ("AD", "Admin"),
    ("AU", "Autor"),
    ("US", "Usuário"),
    ("BL", "Bibliotecário")
]

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email adress", unique=True)
    nome = models.CharField(max_length=100)
    cpf = models.BigIntegerField() 
    grupo = models.CharField(max_length=100, choices=GRUPOS, default="US")  
    foto = models.CharField(max_length=200, null=True) 
    descricao = models.CharField(max_length=200, null=True) 
    qtdLivros = models.IntegerField()

    objects = Gerenciador()
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

FORMATO = [
    ("E", "Ebook"),
    ("F", "Físico")
]

STATUS_LIVRO = [
    ("P", "Pendente"),
    ("C", "Cancelado"),
    ("A", "Aprovado")
]

class Livro(models.Model):
    nome = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    estrelas = models.IntegerField()
    valor = models.DecimalField(max_digits=20, decimal_places=2) 
    qtdDisponivel = models.IntegerField()
    descricao = models.CharField(max_length=250)
    nPaginas = models.IntegerField()
    nEdicao = models.IntegerField()
    nAno = models.IntegerField()
    idFormato = models.CharField(max_length=100, choices=FORMATO, default="E") 
    idStatus = models.CharField(max_length=100, choices=STATUS_LIVRO, default="P") 
    idCategoria = models.ForeignKey(Categoria, related_name="Categoria_Livro", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nome 

class Emprestimo (models.Model):
    idUsuario = models.ForeignKey(CustomUser, related_name="User_Emprestimo", on_delete=models.CASCADE, blank=True, null=True)  
    dtRealizacao = models.DateField(auto_now_add=True, null=False) 
    dtPrevisão = models.DateField(auto_now_add=False, null=False) 
    dtDevolucao = models.DateField(auto_now_add=False, null=True) 
    valorTotal = models.DecimalField(max_digits=20, decimal_places=2) 

    def __str__(self):
        return str(self.idUsuario) + "-" + self.dtRealizacao

class itemEmprestimo(models.Model):
    idEmprestimo = models.ForeignKey(Emprestimo, related_name="Emprestimo_Livro", on_delete=models.CASCADE, blank=True, null=True)
    idLivro = models.ForeignKey(Livro, related_name="Livro_Emprestimo", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.idEmprestimo) + "-" + str(self.idLivro) 