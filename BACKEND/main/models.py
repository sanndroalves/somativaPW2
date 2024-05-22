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
    email = models.EmailField("endereço de email", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    cpf = models.CharField(max_length=20)
    nome = models.CharField(max_length=150)
    foto = models.CharField(max_length=1000, null=False, blank=True)
    descricao = models.CharField(max_length=200, null=False, blank=True)
    qtdLivros = models.IntegerField(default=0)  
    grupo = models.CharField(max_length=100, choices=GRUPOS, default="US")  

    groups = models.ManyToManyField(Group, related_name='custom_user_groups', null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', null=True)

    objects = Gerenciador()

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

SITUACAO = [
    ('E', 'Empréstimo'),
    ('D', 'Devolvido')
]
class Emprestimo (models.Model):
    idUsuario = models.ForeignKey(CustomUser, related_name="User_Emprestimo", on_delete=models.CASCADE, blank=True, null=True)  
    dtRealizacao = models.DateField(auto_now_add=True, null=False) 
    dtPrevisao = models.DateField(auto_now_add=False, blank=True, null=False) 
    dtDevolucao = models.DateField(auto_now_add=False, blank=True, null=True) 
    valorTotal = models.DecimalField(max_digits=20, decimal_places=2) 
    qtdLivros = models.IntegerField(default=0)
    situacao = models.CharField(max_length=100, choices=SITUACAO, default="E") 

    def __str__(self):
        return str(self.idUsuario) + "-" + str(self.dtRealizacao)

class itemEmprestimo(models.Model):
    idEmprestimo = models.ForeignKey(Emprestimo, related_name="Emprestimo_Livro", on_delete=models.CASCADE, blank=True, null=True)
    idLivro = models.ForeignKey(Livro, related_name="Livro_Emprestimo", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.idEmprestimo) + "-" + str(self.idLivro) 