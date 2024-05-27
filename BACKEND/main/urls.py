from .views import CategoriaView, CustomUserView, LivroView, EmprestimoView,itemEmprestimoView
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'categoria',CategoriaView)
router.register(r'livro',LivroView)
router.register(r'emprestimo',EmprestimoView) 
router.register(r'itememprestimo',itemEmprestimoView) 
router.register(r'usuario',CustomUserView) 

urlpatterns = router.urls