<template>
  <div class="page">
    <h1 class="title">📚 Книги по структуре библиотеки</h1>

    <!-- 1. Выбор библиотеки -->
    <div class="filter">
      <label class="label">Библиотека:</label>
      <select v-model="selectedRoot" @change="onRootChange" class="select">
        <option value="">Все библиотеки</option>
        <option v-for="root in roots" :key="root.id" :value="root.id">
          {{ root.name }}
        </option>
      </select>
    </div>

    <!-- 2. Выбор стеллажа -->
    <div class="filter" v-if="selectedRoot">
      <label class="label">Стеллаж:</label>
      <select v-model="selectedRack" @change="onRackChange" class="select">
        <option value="">Все стеллажи</option>
        <option v-for="rack in racks" :key="rack.id" :value="rack.id">
          {{ rack.number || ('Стеллаж #' + rack.id) }}
        </option>
      </select>
    </div>

    <!-- 3. Выбор полки -->
    <div class="filter" v-if="selectedRack">
      <label class="label">Полка:</label>
      <select v-model="selectedSection" @change="loadBooks" class="select">
        <option value="">Все полки</option>
        <option v-for="sec in sections" :key="sec.id" :value="sec.id">
          {{ sec.number || ('Полка #' + sec.id) }}
        </option>
      </select>
    </div>

    <!-- Таблица книг -->
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
            <td>
              <img v-if="book.cover" :src="book.cover" class="cover" />
            </td>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.genre }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.pages }}</td>
            <td>{{ book.rack_number ?? '-' }}</td>
            <td>{{ book.section_number ?? '-' }}</td>
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
import '../assets/css/locations_selects.css'

const API = "http://127.0.0.1:8000"

const roots = ref([])
const racks = ref([])
const sections = ref([])
const books = ref([])

const selectedRoot = ref("")
const selectedRack = ref("")
const selectedSection = ref("")

// -------------------------
// 1. Загрузка библиотек
// -------------------------
const loadRoots = async () => {
  try {
    const res = await axios.get(`${API}/locations/roots/`)
    roots.value = res.data
  } catch (err) {
    console.error("Ошибка загрузки библиотек:", err)
  }
}

// -------------------------
// 2. Загрузка стеллажей выбранной библиотеки
// -------------------------
const loadRacks = async () => {
  if (!selectedRoot.value) {
    racks.value = []
    return
  }
  try {
    const res = await axios.get(`${API}/locations/roots/${selectedRoot.value}/racks/`)
    racks.value = res.data
  } catch (err) {
    console.error("Ошибка загрузки стеллажей:", err)
  }
}

// -------------------------
// 3. Загрузка полок выбранного стеллажа
// -------------------------
const loadSections = async () => {
  if (!selectedRack.value) {
    sections.value = []
    return
  }
  try {
    const res = await axios.get(`${API}/locations/racks/${selectedRack.value}/sections/`)
    sections.value = res.data
  } catch (err) {
    console.error("Ошибка загрузки полок:", err)
  }
}

// -------------------------
// 4. Загрузка книг
// -------------------------
const loadBooks = async () => {
  let url = `${API}/book/` // все книги по умолчанию

  if (selectedSection.value) {
    url = `${API}/book/sections/${selectedSection.value}/books/`
  } else if (selectedRack.value) {
    url = `${API}/book/racks/${selectedRack.value}/books/`
  } else if (selectedRoot.value) {
    url = `${API}/book/roots/${selectedRoot.value}/books/`
  }

  try {
    const res = await axios.get(url)
    books.value = res.data
  } catch (err) {
    console.error("Ошибка загрузки книг:", err)
  }
}

// -------------------------
// Обработчики выбора
// -------------------------
const onRootChange = async () => {
  selectedRack.value = ""
  selectedSection.value = ""
  await loadRacks()
  sections.value = []
  loadBooks()
}

const onRackChange = async () => {
  selectedSection.value = ""
  await loadSections()
  loadBooks()
}

// -------------------------
onMounted(() => {
  loadRoots()
  loadBooks()
})
</script>
