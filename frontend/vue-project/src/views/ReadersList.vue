<template>
  <div class="page">
    <!-- <h1 class="title">👥 Список читателей</h1> -->

    <!-- Кнопка добавления читателя -->
    <button @click="openAddModal" class="btn add">➕ Добавить читателя</button>

    <!-- Таблица читателей -->
    <div v-if="readers.length > 0" class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Email</th>
            <th class="actions-col">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="reader in readers" :key="reader.id">
            <td>{{ reader.id }}</td>
            <td>{{ reader.last_name }} {{ reader.first_name }}</td>
            <td>{{ reader.email }}</td>
            <td class="actions">
              <button @click="startEditReader(reader)" class="btn edit">✏️</button>
              <button @click="deleteReader(reader.id)" class="btn delete">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="empty">
      <p>Читателей пока нет</p>
    </div>

    <!-- Модальное окно редактирования -->
    <div v-if="editingReader" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal">
        <h2 class="modal-title">Редактировать читателя</h2>
        <input v-model="editForm.first_name" placeholder="Имя" class="input" />
        <input v-model="editForm.last_name" placeholder="Фамилия" class="input" />
        <input v-model="editForm.email" placeholder="Email" class="input" />
        <div class="modal-buttons">
          <button @click="saveReader" class="btn save">Сохранить</button>
          <button @click="cancelEdit" class="btn cancel">Отмена</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления -->
    <div v-if="addModal" class="modal-overlay" @click.self="closeAddModal">
      <div class="modal">
        <h2 class="modal-title">Добавить читателя</h2>
        <input v-model="newReader.first_name" placeholder="Имя" class="input" />
        <input v-model="newReader.last_name" placeholder="Фамилия" class="input" />
        <input v-model="newReader.email" placeholder="Email" class="input" />
        <div class="modal-buttons">
          <button @click="createReader" class="btn save">Добавить</button>
          <button @click="closeAddModal" class="btn cancel">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const readers = ref([]);
const editingReader = ref(null);
const editForm = ref({});
const addModal = ref(false);
const newReader = ref({ first_name: "", last_name: "", email: "" });

const loadReaders = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/reader/");
    readers.value = res.data;
  } catch { alert("Ошибка загрузки читателей") }
}

const startEditReader = (reader) => { editingReader.value = reader; editForm.value = { ...reader } }
const cancelEdit = () => { editingReader.value = null; editForm.value = {} }
const saveReader = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/reader/${editingReader.value.id}/`, editForm.value)
    alert("Читатель обновлён!"); cancelEdit(); await loadReaders()
  } catch { alert("Ошибка при сохранении") }
}
const deleteReader = async (id) => {
  if(!confirm("Удалить читателя?")) return
  try { await axios.delete(`http://127.0.0.1:8000/reader/${id}/`); alert("Читатель удалён"); await loadReaders() }
  catch { alert("Ошибка при удалении") }
}

const openAddModal = () => { addModal.value = true }
const closeAddModal = () => { addModal.value = false; newReader.value = { first_name:"", last_name:"", email:"" } }
const createReader = async () => {
  try { await axios.post("http://127.0.0.1:8000/reader/", newReader.value); alert("Читатель добавлен!"); closeAddModal(); await loadReaders() }
  catch { alert("Ошибка при добавлении") }
}

onMounted(loadReaders)
</script>
<style scoped>
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.45); display:flex; justify-content:center; align-items:center; animation:fade 0.2s ease }
.modal { background:white; padding:2rem; border-radius:12px; width:420px; box-shadow:0 4px 16px rgba(0,0,0,0.2); animation:pop 0.25s ease }
.modal-title { margin-bottom:1rem }
.input { width:100%; margin-bottom:1rem; padding:0.7rem; border-radius:8px; border:1px solid #ccc }
.modal-buttons { display:flex; justify-content:space-between }
.empty { text-align:center; margin-top:2rem; color:#777 }
@keyframes fade { from{opacity:0} to{opacity:1} }
@keyframes pop { from{opacity:0; transform:scale(0.9)} to{opacity:1; transform:scale(1)} } 
</style> 
