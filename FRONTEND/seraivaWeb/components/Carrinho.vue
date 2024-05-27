<script setup>
  import { useCartStore } from '@/stores/carrinho';
  import { computed } from 'vue';
  
  const cartStore = useCartStore();
  
  const { cartItems, cartItemCount, removeFromCart, clearCart } = cartStore;
   
  const totalValue = computed(() => {
    return cartItems.reduce((total, item) => total + parseFloat(item.valor), 0).toFixed(2);
  });


  const { data } = useAuth()  
  const idUsuario = ref(JSON.stringify(data.value.results[0].id)) 
 
  const sendEmprestimo = async (itensEmprestimoData) => {

    for (const item of itensEmprestimoData) {
      await sendItemEmprestimo(response.data._rawValue.id, item.id);
    }

    try {
        const response = await useFetch(`http://localhost:8000/emprestimo/`, {
            method: 'POST',
            body: {
                idUsuario: idUsuario,
                valorTotal: totalValue,
                qtdLivros: cartItemCount,
            },
            key: 'emprestimoPost'
        });
 
        if (!response.error.value) { 
            for (const item of itensEmprestimoData) {
                await sendItemEmprestimo(response.data._rawValue.id, item.id);
            }

            clearCart()
        } else {    
            let error = response.error._object.emprestimoPost.data.error
            showError(error)
        }
    } catch (error) {
        console.error("Erro ao enviar o empréstimo:", error); 
        let error2 = response.error._object.emprestimoPost.data.error
        showError(error2)
    }
}

const sendItemEmprestimo = async (idEmprestimo, idLivro) => {
    try {
        const response = await useFetch(`http://localhost:8000/itememprestimo/`, {
            method: 'POST',
            body: {
                idEmprestimo: idEmprestimo,
                idLivro: idLivro
            },
            key: 'itemEmprestimoPost'
        });

        if (!response.error.value) {  
          const {data: dadosLivro } = await useFetch(`http://localhost:8000/livro/${response.data._rawValue.idLivro}`)
          showSuccess(dadosLivro._rawValue.nome)
        } else {    
            console.log("res", response)
            let error = response.error._object.itemEmprestimoPost.data.error
            showError(error)
        }
    } catch (error) {
        console.error("Erro ao enviar o item de empréstimo:", error);
        showError("Erro ao enviar o item de empréstimo.")
    }
}

const toast = useToast();

const showSuccess = (livro) => {
    toast.add({ severity: 'success', summary: 'Empréstimo', detail: `1 livro emprestado com sucesso (${livro})!`, life: 3000 });
}; 

const showError = (msg) => {
    toast.add({ severity: 'error', summary: 'Empréstimo', detail: msg, life: 5000 });
};
   
</script>
<template>
    <div class="cart-wrapper">
      <div class="cart-container">
        <Toast />
        <h1>Carrinho de Compras</h1>
        <div v-if="cartItems.length === 0" class="empty-cart">
          <i class="pi pi-shopping-cart" style="font-size: 50px;"></i>
          <p>Seu carrinho está vazio.</p>
        </div>
        <div v-else>
          <div class="p-grid p-dir-col">
            <div class="p-col" v-for="(item, index) in cartItems" :key="index">
              <div class="cart-item">
                <div class="item-details">
                  <span>{{ item.nome }}</span>
                  <span>{{ item.valor }}</span>
                </div>
                <button @click="removeFromCart(index)" class="p-button p-button-danger">
                  Remover
                  <i class="pi pi-trash" style="margin-left: 4px;"></i>
                </button>
              </div>
            </div>
          </div>
        <div class="total-items">
            <span>Total de itens: {{ cartItemCount }}</span>
            <span>Total: R$ {{ totalValue }}</span>
        </div>
        <div class="total-items">
            <button @click="clearCart()" class="p-button p-button-secondary">
              Limpar Carrinho
              <i class="pi pi-trash" style="margin-left: 4px;"></i>
            </button>
            <button class="p-button p-button-success" @click="sendEmprestimo(cartItems)">
              Emprestar
              <i class="pi pi-arrow-right" style="margin-left: 4px;"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
</template>
  
<style scoped>
  .cart-wrapper {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 10px;
    background-color: #f0f0f0;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .cart-container {
    max-width: 800px;
  }
  
  .empty-cart {
    text-align: center;
  }
  
  .cart-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #ccc;
    padding: 10px;
  }
  
  .item-details {
    display: flex;
    flex-direction: column;
  }
  
  .total-items {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
  }
   
  .p-button-success {
    background-color: #4CAF50;
    color: white;
    border-color: #4CAF50;
  }
  
  .p-button-success:hover {
    background-color: #45a049;
    border-color: #45a049;
  }
  </style>
  