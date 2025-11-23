<template>
  <div class="page">
    <h1 class="title">🏛️ Книги библиотеки</h1>

    <!-- Выбор библиотеки -->
    <div class="filter">
      <label>Выберите библиотеку:</label>
      <select v-model="selectedLocation" @change="loadBooks" class="input">
        <option value="">Все библиотеки</option>
        <option v-for="loc in locationRoots" :key="loc.id" :value="loc.id">{{ loc.name }}</option>
      </select>
    </div>

    <!-- Таблица с книгами -->
    <div v-if="books.length" class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Обложка</th>
            <th>Название</th>
            <th>Автор</th>
            <th>Год</th>
            <th>Жанр</th>
            <th>ISBN</th>
            <th>Страницы</th>
            <th>Стеллаж</th>
            <th>Полка</th>
            <th>Доступно / Всего</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td><img v-if="book.cover" :src="book.cover" class="cover" /></td>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.genre }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.pages }}</td>
            <td>{{ book.rack_number || '-' }}</td>
            <td>{{ book.section_number || '-' }}</td>
            <td>{{ book.available_copies }} / {{ book.total_copies }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty"><p>Книг пока нет</p></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import '../assets/css/books_list.css'

const books = ref([])
const locationRoots = ref([])
const selectedLocation = ref('')

// Загрузка всех библиотек
const loadLocationRoots = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/locations/roots/')
    locationRoots.value = res.data
  } catch(e) {
    console.error('Ошибка загрузки библиотек:', e)
  }
}

// Загрузка книг выбранной библиотеки
const loadBooks = async () => {
  try {
    let url = 'http://127.0.0.1:8000/book/'
    if(selectedLocation.value) {
      url += `?location_root=${selectedLocation.value}` // фильтр по библиотеке
    }
    const res = await axios.get(url)
    books.value = res.data
  } catch(e) {
    console.error('Ошибка загрузки книг:', e)
  }
}

onMounted(() => {
  loadLocationRoots()
  loadBooks()
})
</script>

<style scoped>
.page {
  padding: 20px;
}

.title {
  margin-bottom: 20px;
}

.filter {
  margin-bottom: 15px;
}

.input {
  padding: 6px 8px;
  margin-left: 10px;
}

.table-wrapper {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ccc;
  padding: 6px;
  text-align: left;
}

.cover {
  width: 40px;
  height: 50px;
  object-fit: cover;
}
</style>
