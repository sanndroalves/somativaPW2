<script setup>
  import { useCartStore } from '@/stores/carrinho'; 
  import { ref } from 'vue'; 
  const cartStore = useCartStore(); 
  const { addToCart, cartItems } = cartStore;
  
  const { data: getLivros } = await useFetch('https://somativapw2-production.up.railway.app/livro?idStatus=A');
  const livros = ref(getLivros._rawValue.results); 
  
  const formatLabel = (formato) => {
    const formatMap = {
      E: 'EBOOK',
      F: 'FÍSICO'
    };
    return formatMap[formato] || 'DESCONHECIDO';
  };
  
  let showSuccessMessage = ref(false);
  let showMaxItemsMessage = ref(false);
  
  const addToCartAndShowMessage = (livro) => {
    if (cartItems.length < 3) {
      addToCart(livro);
      showSuccessMessage.value = true;
      setTimeout(() => {
        showSuccessMessage.value = false;
      }, 3000);
    } else {
      showMaxItemsMessage.value = true;
      setTimeout(() => {
        showMaxItemsMessage.value = false;
      }, 3000);
    }
  };

    const { data } = useAuth() 
    const dados = ref( data.value) 

    const verifyLogin = ref(false)
    if(dados.value != undefined){ 
        verifyLogin.value = true
    }
  </script>

<template>
    <div class="container">
      <div class="card-wrapper">
        <Card class="book-card" v-for="livro in livros" :key="livro.id">
          <template #header>
            <div class="header-content">
                <NuxtLink :to="'livros/' + livro.id">
                <img class="book-image" :src="livro.img" alt="Capa do livro" />    
                </NuxtLink>
              
            </div>
          </template>
          <template #title>{{ livro.nome }}</template>
          <template #subtitle>
            <Rating v-model="livro.estrelas" readonly :cancel="false" />
          </template>
          <template #content>
            <div class="book-details">
              <table class="details-table">
                <tr>
                  <th>ANO:</th>
                  <td>{{ livro.nAno }}</td>
                </tr>
                <tr>
                  <th>EDIÇÃO:</th>
                  <td>{{ livro.nEdicao }}</td>
                </tr>
                <tr>
                  <th>PÁG:</th>
                  <td>{{ livro.nPaginas }}</td>
                </tr>
                <tr>
                  <th>CATEGORIA:</th>
                  <td>{{ livro.idCategoria }}</td>
                </tr>
                <tr>
                  <th>FORMATO:</th>
                  <td>{{ formatLabel(livro.idFormato) }}</td>
                </tr>
              </table>
              <p class="book-description">{{ livro.descricao }}</p>
            </div>
          </template>
          <template #footer v-if="verifyLogin">
            <div v-if="livro.qtdDisponivel > 0">
              <Button @click="addToCartAndShowMessage(livro)" label="Comprar" class="buy-button" />
            </div>
            <div v-else>
              <span class="unavailable-label">Indisponível</span>
            </div>
          </template>
          <template #footer v-else>
            <span class="unlogin-label">Faça login</span>
          </template>
        </Card>
      </div>
      <Message v-if="showSuccessMessage" severity="success" class="success-message">
        Item adicionado ao carrinho com sucesso!
      </Message>
      <Message v-if="showMaxItemsMessage" severity="warn" class="max-items-message">
        O carrinho está cheio. Limite de 3 itens atingido.
      </Message>
    </div>
  </template>
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
    padding: 50px;
  }
  
  .card-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
  }
  
  .book-card {
    width: 300px;
    overflow: hidden;
  }
  
  .header-content {
    text-align: center;
    padding: 20px;
  }
  
  .book-image {
    max-width: 100%;
    max-height: 200px;
    object-fit: contain;
  }
  
  .book-details {
    margin: 20px 0;
  }
  
  .details-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .details-table th,
  .details-table td {
    text-align: left;
    padding: 5px;
    border-bottom: 1px solid #ccc;
  }
  
  .book-description {
    margin-top: 20px;
    font-size: 14px;
    line-height: 1.5;
  }
  
  .buy-button {
    width: 100%;
    margin-top: 10px;
  }
  
  .unavailable-label {
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 10px 0;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    margin-top: 10px;
  }

  .unlogin-label {
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 10px 0;
    background-color: #f3f8d7;
    color: #8a8519;
    border: 1px solid #eeff8f;
    border-radius: 4px; 
  }
  
  .success-message {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .max-items-message {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
  }
  </style>
  