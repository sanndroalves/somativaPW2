from django.shortcuts import render
from .models import *
from .serializers import *
from .customFilters import *
import datetime 

from rest_framework import filters  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

class CustomModelViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomUserFilter
    # permission_classes = (IsAuthenticated,)

class CategoriaView(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer 

class LivroView(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LivroFilter

class EmprestimoView(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmprestimoFilter

    def create(self, request, *args, **kwargs):
        # 1 - verifica se tem empréstimo atrasado
        # 2 - verifica a qtdLivros que o usuário já tem
        # 3 - realiza o empréstimo

        data = request.data
        idUsuario = request.data.get('idUsuario')
        
        usuario_info = CustomUser.objects.filter(id=idUsuario).first() 
        if not usuario_info:
            return Response({"error": f"Usuário não encontrado."}, status=400)
        # 1 - VERIFICAR SE TEM ALGUM EMPRESTIMO PENDENTE
        hoje = datetime.date.today()
        emprestimos_pendentes = Emprestimo.objects.filter(
            idUsuario=idUsuario, 
            dtPrevisao__lt=hoje, 
            dtDevolucao__isnull=True
        )

        if emprestimos_pendentes.exists():
            return Response({"error": "Usuário possui empréstimos pendentes."}, status=400)
        
        # 2 - VERIFICAR QTD DE LIVROS EMPRESTADOS
        if usuario_info and usuario_info.qtdLivros < 3:
            qtd_livros_novos = int(data.get('qtdLivros', 0))   
            soma = qtd_livros_novos + usuario_info.qtdLivros
            if soma > 3:
                return Response(
                    {"error": f"Você não pode ultrapassar o limite de 3 livros emprestados. Diminua a quantidade, você já possui: {usuario_info.qtdLivros} emprestados."},
                    status=409
                )
            else:
                usuario_info.qtdLivros += qtd_livros_novos
                usuario_info.save()

                data_realizacao = datetime.date.today()
                data_previsao = data_realizacao + datetime.timedelta(weeks=2)

                request.data['dtRealizacao'] = data_realizacao
                request.data['dtPrevisao'] = data_previsao

                serializer = EmprestimoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                else:
                    return Response(serializer.errors, status=400)

        return Response({"error": "Usuário não pode emprestar mais livros."}, status=400)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        dtDevolucao = request.data.get('dtDevolucao', None)
        
        if dtDevolucao:
            idUsuario = instance.idUsuario
            
            usuario_info = CustomUser.objects.filter(email=idUsuario).first() 
            usuario_info.qtdLivros -= instance.qtdLivros
            if usuario_info.qtdLivros < 0:
                raise ValidationError("qtLivros não pode ser negativa.")
            
            usuario_info.save()

        response = super().partial_update(request, *args, **kwargs)
        
        return response

class itemEmprestimoView(viewsets.ModelViewSet):
    queryset = itemEmprestimo.objects.all()
    serializer_class = itemEmprestimoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        idLivro = data.get('idLivro')

        if not idLivro:
            return Response({"error": "ID do livro não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        livro = Livro.objects.filter(id=idLivro).first()

        if not livro:
            return Response({"error": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if livro.qtdDisponivel < 1:
            return Response({"error": "Livro sem estoque disponível."}, status=status.HTTP_400_BAD_REQUEST)

        livro.qtdDisponivel -= 1
        livro.save()

        serializer = itemEmprestimoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

