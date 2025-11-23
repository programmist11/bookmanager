<template>
  <div v-if="modalOpen" class="modal-overlay">
    <div class="modal">
      <h2 class="modal-title">{{ editingBook ? 'Редактировать книгу' : 'Добавить книгу' }}</h2>

      <!-- Прокручиваемая область формы -->
      <div class="modal-content">
        <input v-model="form.title" placeholder="Название" class="input" @input="searchBook" />
        <ul v-if="suggestions.length" class="suggestions">
          <li v-for="s in suggestions" :key="s.title + s.author" @click="fillBook(s)">
            <img v-if="s.cover" :src="s.cover" class="mini-cover" /> {{ s.title }} — {{ s.author }} ({{ s.year }})
          </li>
        </ul>

        <input v-model="form.author" placeholder="Автор" class="input" />
        <input v-model="form.year" type="number" placeholder="Год" class="input" />
        <input v-model="form.genre" placeholder="Жанр" class="input" />
        <input v-model="form.isbn" placeholder="ISBN" class="input" />
        <input v-model.number="form.pages" type="number" placeholder="Страницы" class="input" />
        <textarea v-model="form.description" placeholder="Описание" class="input"></textarea>
        <input v-model="form.cover" placeholder="URL обложки" class="input" />
        <input v-model.number="form.total_copies" type="number" placeholder="Всего копий" class="input" />
        <input v-model.number="form.available_copies" type="number" placeholder="Доступно копий" class="input" />

        <select v-model="form.location_root" class="input" @change="loadRacks">
          <option value="">Выберите библиотеку</option>
          <option v-for="root in locationRoots" :key="root.id" :value="root.id">{{ root.name }}</option>
        </select>

        <select v-model="form.rack" class="input" @change="loadSections">
          <option value="">Выберите стеллаж</option>
          <option v-for="rack in racks" :key="rack.id" :value="rack.id">{{ rack.number }}</option>
        </select>

        <select v-model="form.section" class="input">
          <option value="">Выберите полку</option>
          <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.number }}</option>
        </select>
      </div>

      <div class="modal-buttons">
        <button @click="$emit('submitBook', form)" class="btn save">{{ editingBook ? 'Сохранить' : 'Добавить' }}</button>
        <button @click="$emit('closeModal')" class="btn cancel">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

defineProps({
  modalOpen: Boolean,
  editingBook: Object,
  form: Object,
  locationRoots: Array,
  racks: Array,
  sections: Array,
  suggestions: Array
})

const emit = defineEmits(['closeModal', 'submitBook'])

const loadRacks = async () => emit('loadRacks')
const loadSections = async () => emit('loadSections')
const searchBook = async () => emit('searchBook')
const fillBook = (bookData) => emit('fillBook', bookData)
</script>

<style scoped>
.modal {
  max-height: 80vh; /* Ограничиваем высоту окна */
  width: 500px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.modal-content {
  overflow-y: auto; /* Включаем вертикальный скролл */
  max-height: 60vh; /* Максимальная высота формы */
  margin-bottom: 15px; /* Отступ перед кнопками */
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  box-sizing: border-box;
}

.suggestions {
  list-style: none;
  padding: 0;
  margin: 0 0 10px 0;
  max-height: 150px;
  overflow-y: auto;
}

.mini-cover {
  width: 30px;
  height: 40px;
  object-fit: cover;
  margin-right: 5px;
}
</style>
