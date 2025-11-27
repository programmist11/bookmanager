<template>
  <div class="page">
    <button @click="openModal()" class="btn add">➕ Добавить книгу</button>

    <BookTable 
      :books="books" 
      @editBook="openModal" 
      @deleteBook="deleteBook" 
    />

    <BookModal 
      :modalOpen="modalOpen" 
      :editingBook="editingBook" 
      :form="form"
      :locationRoots="locationRoots"
      :racks="racks"
      :sections="sections"
      :suggestions="suggestions"
      @closeModal="closeModal"
      @submitBook="submitBook"
      @loadRacks="loadRacks"
      @loadSections="loadSections"
      @searchBook="searchBook"
      @fillBook="fillBook"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import '../assets/css/books_list.css'
import BookModal from './BookModal.vue'
import BookTable from './BookTable.vue'

const books = ref([])
const modalOpen = ref(false)
const editingBook = ref(null)
const form = ref({
  title:'', author:'', year:'', genre:'', description:'', cover:'', isbn:'', pages:0,
  total_copies:1, available_copies:1, location_root:'', rack:'', section:''
})
const suggestions = ref([])

const locationRoots = ref([])
const racks = ref([])
const sections = ref([])

// --- Загрузка списка книг ---
const loadBooks = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/book/')
    books.value = res.data
  } catch(e) {
    console.error('Ошибка загрузки книг:', e)
  }
}

// --- Загрузка библиотек ---
const loadLocationRoots = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/locations/roots/')
    locationRoots.value = res.data
  } catch(e){ console.error(e) }
}

// --- Загрузка стеллажей ---
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

// --- Загрузка полок ---
const loadSections = async () => {
  if(!form.value.rack) { sections.value = []; return }
  try {
    const res = await axios.get(`http://127.0.0.1:8000/locations/racks/${form.value.rack}/sections/`)
    sections.value = res.data
    form.value.section = ''
  } catch(e){ console.error(e) }
}

// --- Открытие модального окна ---
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

// --- Закрытие модального окна ---
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

// --- Добавление или редактирование книги ---
const submitBook = async (formData) => {
  try {
    const payload = {
      ...formData,
      location_root: formData.location_root || null,
      rack: formData.rack || null,
      section: formData.section || null
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
  } catch(e){
    console.error('Ошибка при сохранении книги:', e)
    alert("Ошибка при сохранении")
  }
}

// --- Удаление книги ---
const deleteBook = async (id) => {
  if(!confirm("Удалить книгу?")) return
  try { 
    await axios.delete(`http://127.0.0.1:8000/book/${id}/`)
    await loadBooks() 
  } catch(e){
    console.error('Ошибка при удалении книги:', e)
    alert("Ошибка при удалении")
  }
}

// --- Автодополнение по названию ---
const searchBook = async () => {
  if(form.value.title.length < 3){ suggestions.value = []; return }
  try {
    const res = await axios.get("http://127.0.0.1:8000/book/autocomplete/", { params: { title: form.value.title } })
    suggestions.value = res.data
  } catch(e){ console.error(e) }
}

// --- Заполнение формы данными из автодополнения ---
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

// --- Инициализация ---
onMounted(() => {
  loadBooks()
  loadLocationRoots()
})
</script>
