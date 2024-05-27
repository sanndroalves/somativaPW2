<template>
    <div class="header">
      <div class="logo">
        <Image src="https://lojasaraivanew.vtexassets.com/assets/vtex/assets-builder/lojasaraivanew.lojasaraivanew-theme/2.0.4/icons/saraiva-logo___38928680236d66f6452775c48c8a4750.svg" alt="Image" width="250" />
      </div>
      <div class="navigation">
        <TabMenu :model="items" />
      </div>
      <div class="avatar-group" v-if="verifyLogin">
        <Avatar icon="pi pi-shopping-cart" class="cart-avatar" style="background-color: #4CAF50;" @click="goToCart" />
        <div class="dropdown">
          <Avatar icon="pi pi-user" class="user-avatar" @click="toggleDropdown" />
          <div class="dropdown-content" v-show="showDropdown">
            <ul>
                <li @click="addBook" v-if="Grupo == 'AU' || Grupo == 'AD'" @mouseover="highlightItem" @mouseout="resetItem" ref="addBook">Adicionar Livro</li>
                <li @click="submitLogout" @mouseover="highlightItem" @mouseout="resetItem" ref="logout">Sair</li>
            </ul>
          </div>
        </div> 
      </div>
      <div v-else>
            <Avatar icon="pi pi-user" class="cart-avatar" style="margin-left: 25px;background-color: #4CAF50;" @click="login" />
        </div>
    </div> 
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router'; 
  
  const router = useRouter();
  
  const items = ref([
    { label: 'Início', icon: 'pi pi-home', command: () => router.push('../') },
    { label: 'Livros', icon: 'pi pi-book', command: () => router.push('/livros') }, 
  ]);
  
  const goToCart = () => {
    router.push('/carrinho');
  };

  const login = () => {
    router.push('/auth');
  };
  
    const { data } = useAuth() 
    const dados = ref( data.value) 
    const Grupo = ref()
    const verifyLogin = ref(false)
    if(dados.value != undefined){ 
        verifyLogin.value = true
        const idUsuario = ref(JSON.stringify(data.value.results[0].id))
        const { data: dadosUsuario } = await useFetch(`http://localhost:8000/usuario/${idUsuario.value}`); 
        Grupo.value = dadosUsuario._rawValue.grupo 

        items.value.push({ label: 'Empréstimos', icon: 'pi pi-list', command: () => router.push('/emprestimos') });
    }

    const addBook = () => {
        router.push('/livros/cadastro');
    };
  
  const { signOut } = useAuth();

    const submitLogout = ()=> {
        signOut({redirect: false}).then(()=>{
            console.log("successfully performed the logout");
            navigateTo("/auth")
        }).catch((error)=>{
            console.log("error when trying logout ", error);
        })
    }
  
  const showDropdown = ref(false);
  
  const toggleDropdown = () => {
    showDropdown.value = !showDropdown.value;
  };

  const highlightItem = (event) => {
  event.target.style.backgroundColor = '#f0f0f0';
};

const resetItem = (event) => {
  event.target.style.backgroundColor = '';
};
  </script>
  
  <style scoped>
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
  }
  
  .logo {
    flex: 1;
    text-align: center;
    margin-right: 25px;
  }
  
  .navigation {
    flex: 3;
  }
  
  .avatar-group {
    position: relative;
    margin-right: 150px;
    margin-left: 25px;
  }
  
  .cart-avatar {
    margin-right: 10px;
    color: white;
  }
  
  .user-avatar {
    cursor: pointer;
  }
  
  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  .dropdown-content { 
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }
  
  .dropdown-content ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .dropdown-content ul li {
    padding: 8px 12px;
    cursor: pointer;
  }
  
  .dropdown:hover .dropdown-content {
    display: block;
  }
  </style>
  