<script setup>
import { ref } from 'vue';

const { data } = useAuth()  
const idUsuario = ref(JSON.stringify(data.value.results[0].id))
const { data: dadosUsuario } = await useFetch(`http://localhost:8000/usuario/${idUsuario.value}`); 
const Grupo = dadosUsuario._rawValue.grupo 

const { data: emprestimos } = await useFetch(`http://localhost:8000/emprestimo?idUsuario=${idUsuario.value}`);
const getEmprestimos = emprestimos._rawValue.results;

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
};

const email = ref('');
const loans = ref([]);
const searched = ref(false);

const idPesquisa = ref()
const searchLoans = async () => {
  searched.value = false;
  loans.value = [];

  const {data: dadosUsuarioPesquisa } = await useFetch(`http://localhost:8000/usuario?email=${email.value}`)
  idPesquisa.value = dadosUsuarioPesquisa._rawValue.results[0].id

  try {
    const response = await useFetch(`http://localhost:8000/emprestimo?idUsuario=${idPesquisa.value}`, {
      method: 'GET'
    });

    if (!response.error.value) {
      loans.value = response.data._rawValue.results;
      searched.value = true;
    } else {
      showError(response.error.value);
    }
  } catch (error) {
    console.error("Erro ao buscar empréstimos:", error);
    showError("Erro ao buscar empréstimos. Por favor, tente novamente mais tarde.");
  }
};

const addDevolucao = async (loan) => {
  const formatDateBackEnd = (date) => {
    const d = new Date(date);
    const month = `${d.getMonth() + 1}`.padStart(2, '0');
    const day = `${d.getDate()}`.padStart(2, '0');
    const year = d.getFullYear();
    return `${year}-${month}-${day}`;
  };
  try {
    const formattedDate = formatDateBackEnd(loan.dtDevolucao);
    const response = await useFetch(`http://localhost:8000/emprestimo/${loan.id}/`, {
      method: 'PATCH',
      body: { dtDevolucao: formattedDate, idUsuario: loan.idUsuario, qtdLivros: loan.qtdLivros  },
      key: 'updateDevolucao'
    });

    if (!response.error.value) {
      showSuccess("Data de devolução adicionada com sucesso.");
    } else {
      showError(response.error.value);
    }
  } catch (error) {
    console.error("Erro ao adicionar data de devolução:", error);
    showError("Erro ao adicionar data de devolução. Por favor, tente novamente mais tarde.");
  }
};

const toast = useToast();
const showSuccess = () => {
    toast.add({ severity: 'success', summary: 'Empréstimo', detail: 'Data adicionada com sucesso!', life: 3000 });
}; 

const showError = (msg) => {
    toast.add({ severity: 'error', summary: 'Empréstimo', detail: msg, life: 5000 });
};
</script>

<template>
  <div class="emprestimos-container" v-if="Grupo == 'US'">
    <h1>Meus Empréstimos</h1>
    <table class="emprestimos-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Data de Realização</th>
          <th>Data Prevista Devolução</th>
          <th>Quantidade de Livros</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="emprestimo in getEmprestimos" :key="emprestimo.id">
          <td>{{ emprestimo.id }}</td>
          <td>{{ formatDate(emprestimo.dtRealizacao) }}</td>
          <td>{{ formatDate(emprestimo.dtPrevisao) }}</td>
          <td>{{ emprestimo.qtdLivros }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="search-loan-container" v-else-if="Grupo == 'BL'">
    <Toast />
    <div class="search-loan-card">
      <h1 class="search-loan-title">Pesquisar Empréstimos</h1>
      <div class="form-group">
        <label for="email">Email do Usuário:</label>
        <InputText v-model="email" placeholder="Digite o email do usuário" />
        <Button label="Pesquisar" class="p-button-primary" @click="searchLoans" />
      </div>
      <div v-if="loans.length">
        <DataTable :value="loans" class="p-datatable-gridlines">
          <Column field="id" header="ID" /> 
          <Column field="dtRealizacao" header="Data de Empréstimo" />
          <Column field="valorTotal" header="Valor Total" />
          <Column field="qtdLivros" header="Quantidade de Livros" />
          <Column header="Data de Devolução">
            <template #body="slotProps">
              <Calendar v-model="slotProps.data.dtDevolucao" />
            </template>
          </Column>
          <Column header="Adicionar dtDevolucao">
            <template #body="slotProps">
              <Button label="Adiconar" @click="addDevolucao(slotProps.data)" class="p-button-success" />
            </template>
          </Column>
        </DataTable>
      </div>
      <div v-else>
        <p v-if="searched">Nenhum empréstimo encontrado para o email fornecido.</p>
      </div>
    </div>
  </div>
  <div v-else>
    Você não acesso a esta área.   
  </div>
</template>

<style scoped>
.emprestimos-container {
  margin: 50px auto;
  width: 80%;
}

.emprestimos-table {
  width: 100%;
  border-collapse: collapse;
}

.emprestimos-table th,
.emprestimos-table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.emprestimos-table th {
  background-color: #f2f2f2;
}

.search-loan-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
}

.search-loan-card {
  width: 800px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.search-loan-title {
  text-align: center;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-group label {
  margin-right: 10px;
}

.form-group .p-inputtext {
  margin-right: 10px;
}

.p-datatable-gridlines {
  margin-top: 20px;
}
</style>
