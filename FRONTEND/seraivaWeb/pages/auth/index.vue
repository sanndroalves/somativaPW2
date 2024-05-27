<script setup>
import { reactive, ref } from 'vue';
const { signIn } = useAuth();

definePageMeta({
    layout: 'login'
})



const credenciais = reactive({
    email: '',
    password: ''
});
const mensagemErro = ref('');

const fazerLogin = () => {
    signIn(credenciais, { redirect: false })
        .then(() => {
            console.log("logado com sucesso....");
            navigateTo('/');
        })
        .catch((error) => {
            console.error("error: ", error);
            mensagemErro.value = 'Não foi possível fazer o login com estas credenciais...';
            setTimeout(() => {
                mensagemErro.value = '';
                credenciais.email = '';
                credenciais.password = '';
            }, 3000);
        })
}


const painel = ref();

 
</script>

<template>
    <div class="login-container">
      <div class="login-card">
        <h1 class="login-title">LOGIN</h1>
        <h2 class="login-subtitle">Faça login abaixo</h2>
        <div class="input-group">
          <InputText  v-model="credenciais.email" type="email" placeholder="Email" />
        </div>
        <div class="input-group">
          <Password v-model="credenciais.password"  placeholder="Senha" :feedback="false" />
        </div>
        <div class="button-group">
          <Button @click="fazerLogin"  label="Entrar" class="p-button-primary" />
        </div>
        <div class="row-login" v-if="mensagemErro !== ''">
                <p id="erro">{{ mensagemErro }}</p>
            </div>
      </div>
    </div>
  </template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0; /* Cor raza */
}

.login-card {
  width: 300px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.login-title {
  text-align: center;
  margin-bottom: 10px;
}

.login-subtitle {
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.button-group {
  display: flex;
  justify-content: center;
}
</style>