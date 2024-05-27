<script setup>
    const { data } = useAuth()  
    const idUsuario = ref(JSON.stringify(data.value.results[0].id))
    const { data: dadosUsuario } = await useFetch(`https://somativapw2-production.up.railway.app/usuario/${idUsuario.value}`);
    const { data: dadosCategorias } = await useFetch(`https://somativapw2-production.up.railway.app/categoria/`);
    const Grupo = dadosUsuario._rawValue.grupo 
    const categorias = dadosCategorias._rawValue.results
    console.log("CA", categorias)

    definePageMeta({
        middleware: "auth",
    });

   const nome = ref()
   const img = ref()
   const estrelas = ref() 
   const valor = ref() 
   const qtdDisponivel = ref() 
   const descricao = ref() 
   const nPaginas = ref() 
   const nEdicao = ref() 
   const nAno = ref() 
   const idFormato = ref() 
   const idCategoria = ref() 

const formatoOptions = [
  { label: 'Ebook', value: 'E' },
  { label: 'Físico', value: 'F' },
];
  
const sendLivro = async () => {
    const livroData = {
      nome: nome.value,
      img: img.value,
      estrelas: estrelas.value,
      valor: valor.value,
      qtdDisponivel: qtdDisponivel.value,
      descricao: descricao.value,
      nPaginas: nPaginas.value,
      nEdicao: nEdicao.value,
      nAno: nAno.value,
      idFormato: idFormato.value,
      idCategoria: idCategoria.value,
      idAutor: idUsuario.value
    };
    
    try {const response = await useFetch(`https://somativapw2-production.up.railway.app/livro/`, {
      method: 'POST',
      body: livroData,
      key: 'livroPost'
    });

    // Verifique se a resposta foi bem-sucedida
    if (!response.error.value) {
      showSuccess();
    } else {
      let error = response.error._object.livroPost.data.error;
      showError(error);
    }
  } catch (error) {
    console.error("Erro ao enviar o livro:", error);
    showError("Erro ao enviar o livro. Por favor, tente novamente mais tarde.");
  }
};

const toast = useToast();

const showSuccess = () => {
    toast.add({ severity: 'success', summary: 'Livro', detail: 'Cadastro com sucesso!', life: 3000 });
}; 

const showError = (msg) => {
    toast.add({ severity: 'error', summary: 'Livro', detail: msg, life: 5000 });
};




</script>

<template>
    <div>
        <Toast />
        <template v-if="Grupo == 'AD' || Grupo == 'AU'">  
            <div class="add-book-container">
                <div class="add-book-card">
                <h1 class="add-book-title">Adicionando Livro</h1>
                <form @submit.prevent="submitForm">
                    <div class="form-group">
                    <div class="input-group">
                        <label for="nome">Nome:</label><br>
                        <InputText v-model="nome" />
                    </div>
                    <div class="input-group">
                        <label for="img">Imagem:</label><br>
                        <InputText v-model="img" />
                    </div>
                    <div class="input-group">
                        <label for="estrelas">Estrelas:</label><br>
                        <InputNumber v-model="estrelas" />
                    </div>
                    </div>
                    <div class="form-group">
                    <div class="input-group">
                        <label for="valor">Valor:</label><br>
                        <InputNumber v-model="valor" mode="currency" currency="BRL" locale="pt-BR" />
                    </div>
                    <div class="input-group">
                        <label for="qtdDisponivel">Quantidade Disponível:</label><br>
                        <InputNumber v-model="qtdDisponivel" />
                    </div>
                    <div class="input-group">
                        <label for="descricao">Descrição:</label><br>
                        <InputText v-model="descricao"   />
                    </div>
                    </div>
                    <div class="form-group">
                    <div class="input-group">
                        <label for="nPaginas">Número de Páginas:</label><br>
                        <InputNumber v-model="nPaginas" />
                    </div>
                    <div class="input-group">
                        <label for="nEdicao">Número de Edição:</label><br>
                        <InputNumber v-model="nEdicao" />
                    </div>
                    <div class="input-group">
                        <label for="nAno">Ano:</label><br>
                        <InputNumber v-model="nAno" />
                    </div>
                    </div>
                    <div class="form-group">
                    <div class="input-group">
                        <label for="idFormato">Formato:</label><br>
                        <Dropdown v-model="idFormato" :options="formatoOptions" optionLabel="label" optionValue="value" />
                    </div> 
                    <div class="input-group">
                        <label for="idCategoria">Categoria:</label><br>
                        <Dropdown v-model="idCategoria" :options="categorias" optionLabel="nome" optionValue="id" />
                    </div>
                    </div>
                    <div class="button-group">
                    <Button  @click="sendLivro" label="Adicionar Livro" class="p-button-primary" />
                    </div>
                </form>
                </div>
            </div> 
        </template>
        <template v-else>
            Você não tem acesso a essa área.
        </template>
    </div>
</template>

<style scoped>
.add-book-container {
  display: flex;
  justify-content: center;
  align-items: center; 
  margin-top: 50px;
}

.add-book-card {
  width: 1000px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.add-book-title {
  text-align: center;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-wrap: wrap;
}

.input-group {
  flex: 1;
  margin-right: 20px;
  margin-bottom: 15px;
}

.button-group {
  display: flex;
  justify-content: center;
}
</style>