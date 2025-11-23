<template>
  <div class="page">
    <h1 class="title">📚 Список книг</h1>
    <button @click="openModal()" class="btn add">➕ Добавить книгу</button>

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
            <th>Библиотека</th>
            <th>Стеллаж</th>
            <th>Полка</th>
            <th>Доступно / Всего</th>
            <th class="actions-col">Действия</th>
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
            <td>{{ book.location_root_name || '-' }}</td>
            <td>{{ book.rack_number || '-' }}</td>
            <td>{{ book.section_number || '-' }}</td>
            <td>{{ book.available_copies }} / {{ book.total_copies }}</td>
            <td>
              <button @click="openModal(book)" class="btn edit">✏️</button>
              <button @click="deleteBook(book.id)" class="btn delete">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty"><p>Книг пока нет</p></div>

    <!-- Модальное окно -->
    <div v-if="modalOpen" class="modal-overlay">
      <div class="modal">
        <h2 class="modal-title">{{ editingBook ? 'Редактировать книгу' : 'Добавить книгу' }}</h2>

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

        <!-- Селекторы локации -->
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

        <div class="modal-buttons">
          <button @click="submitBook" class="btn save">{{ editingBook ? 'Сохранить' : 'Добавить' }}</button>
          <button @click="closeModal" class="btn cancel">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import '../assets/css/books_list.css'

const books = ref([])
const modalOpen = ref(false)
const editingBook = ref(null)
const form = ref({
  title: '', author:'', year:'', genre:'', description:'', cover:'', isbn:'', pages:0,
  total_copies:1, available_copies:1, location_root:'', rack:'', section:''
})
const suggestions = ref([])

const locationRoots = ref([])
const racks = ref([])
const sections = ref([])

// Загрузка книг
const loadBooks = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/book/')
    books.value = res.data
  } catch(e){ console.error(e) }
}

// Загрузка локаций
const loadLocationRoots = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/locations/roots/')
    locationRoots.value = res.data
  } catch(e){ console.error(e) }
}

// Загрузка стеллажей по root
const loadRacks = async () => {
  if(!form.value.location_root) { racks.value = []; return }
  try {
    const res = await axios.get(`http://127.0.0.1:8000/locations/roots/${form.value.location_root}/racks/`)
    racks.value = res.data
    sections.value = []
    form.value.rack = ''
    form.value.section = ''
  } catch(e){ console.error(e) }
}

// Загрузка полок по rack
const loadSections = async () => {
  if(!form.value.rack) { sections.value = []; return }
  try {
    const res = await axios.get(`http://127.0.0.1:8000/locations/racks/${form.value.rack}/sections/`)
    sections.value = res.data
    form.value.section = ''
  } catch(e){ console.error(e) }
}

const openModal = (book=null) => {
  modalOpen.value = true
  if(book){
    editingBook.value = book
    form.value = {
      ...book,
      location_root: book.location_root?.id || '',
      rack: book.rack?.id || '',
      section: book.section?.id || ''
    }
    loadRacks()
    loadSections()
  } else {
    editingBook.value = null
    form.value = {
      title:'', author:'', year:'', genre:'', description:'', cover:'', isbn:'', pages:0,
      total_copies:1, available_copies:1, location_root:'', rack:'', section:''
    }
    racks.value = []
    sections.value = []
  }
}

const closeModal = () => {
  modalOpen.value = false
  form.value = {
    title:'', author:'', year:'', genre:'', description:'', cover:'', isbn:'', pages:0,
    total_copies:1, available_copies:1, location_root:'', rack:'', section:''
  }
  suggestions.value = []
  editingBook.value = null
  racks.value = []
  sections.value = []
}

const submitBook = async () => {
  try {
    const payload = {
      ...form.value,
      location_root: form.value.location_root || null,
      rack: form.value.rack || null,
      section: form.value.section || null
    }

    if(editingBook.value){
      await axios.put(`http://127.0.0.1:8000/book/${editingBook.value.id}/`, payload)
      alert("Книга обновлена!")
    } else {
      await axios.post("http://127.0.0.1:8000/book/", payload)
      alert("Книга добавлена!")
    }
    closeModal()
    await loadBooks()
  } catch(e){ alert("Ошибка при сохранении") }
}

const deleteBook = async (id) => {
  if(!confirm("Удалить книгу?")) return
  try { await axios.delete(`http://127.0.0.1:8000/book/${id}/`); await loadBooks() } 
  catch(e){ alert("Ошибка при удалении") }
}

// Автодополнение по названию
const searchBook = async () => {
  if(form.value.title.length < 3){ suggestions.value = []; return }
  try {
    const res = await axios.get("http://127.0.0.1:8000/book/autocomplete/", { params: { title: form.value.title } })
    suggestions.value = res.data
  } catch(e){ console.error(e) }
}

const fillBook = (bookData) => {
  form.value.title = bookData.title
  form.value.author = bookData.author
  form.value.year = bookData.year || ''
  form.value.genre = bookData.genre || ''
  form.value.description = bookData.description || ''
  form.value.cover = bookData.cover || ''
  form.value.isbn = bookData.isbn || ''
  form.value.pages = bookData.pages || 0
  form.value.total_copies = bookData.total_copies || 5
  form.value.available_copies = bookData.available_copies || 5
  suggestions.value = []
}

onMounted(() => {
  loadBooks()
  loadLocationRoots()
})
</script>
