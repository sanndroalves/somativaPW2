<script setup>
    import { useRoute } from 'vue-router'; 
    const route = useRoute();
    const livroId = route.params.id;
    const { data: livro } = await useFetch(`http://127.0.0.1:8000/livro/${livroId}`);
    const { data: autor } = await useFetch(`http://127.0.0.1:8000/usuario/${livro.value.idAutor}`);
    console.log("AUTOR", autor.value)

    const formatLabel = (formato) => {
    const formatMap = {
        E: 'EBOOK',
        F: 'FÍSICO'
    };
    return formatMap[formato] || 'DESCONHECIDO';
    };
</script>]

<template>
    <div class="pagina-livro">
    <h1>{{ livro.nome }}</h1>
      <div class="conteudo">
        <img :src="livro.img" alt="Capa do Livro" class="livro-imagem" />
        <div class="informacoes-livro">
            <div style="align-items: center; text-align: center;">
                <b>LIVRO</b>
            </div>
          <p><b>Estrelas:</b> {{ livro.estrelas }}</p>
          <p><b>Valor:</b> R$ {{ livro.valor }}</p>
          <p><b>Quantidade Disponível:</b> {{ livro.qtdDisponivel }}</p>
          <p><b>Número de Páginas:</b> {{ livro.nPaginas }}</p>
          <p><b>Número de Edição:</b> {{ livro.nEdicao }}</p>
          <p><b>Ano de Publicação:</b> {{ livro.nAno }}</p>
          <p><b>Formato:</b> {{ formatLabel(livro.idFormato) }}</p>
          <p><b>Descrição:</b> {{ livro.descricao }}</p>
          <br>
          <div style="align-items: center; text-align: center;">
            <b>AUTOR</b>
          </div>
            <div class="autor">
                <img :src="autor.foto" alt="Foto do Autor" class="autor-imagem" /> 
                <div class="autor-informacoes">
                    <h4>{{ autor.nome }}</h4>
                    <span>{{ autor.descricao }}</span>
                </div>
            </div>
        </div>
      </div>
    </div>
  </template>
  
  
  <style scoped>
  .pagina-livro { 
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adiciona sombra */
  background-color: #e3ffee; /* Cor de fundo */
}
  
  .conteudo {
    display: flex;
  }
  
  .livro-imagem {
    max-width: 400px;
    height: auto;
    margin-right: 20px;
  }
  
  .informacoes-livro {
    flex: 1;
  }

.autor {
  display: flex; 
}

.autor-imagem {
  margin-top: 60px;
  max-width: 100px;
  height: 100px;
}

.autor-informacoes {
  margin-left: 10px;
}
  </style>
  