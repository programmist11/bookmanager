<template>
  <div>
    <h1>Выдать книгу</h1>

    <!-- Выбор книги -->
    <select v-model="loan.book" class="select">
      <option disabled value="">Выберите книгу</option>
      <option v-for="b in books" :key="b.id" :value="b.id">
        {{ b.title }} (доступно: {{ b.available_copies }})
      </option>
    </select>

    <!-- Выбор читателя -->
    <select v-model="loan.reader" class="select">
      <option disabled value="">Выберите читателя</option>
      <option v-for="r in readers" :key="r.id" :value="r.id">
        {{ r.last_name }} {{ r.first_name }}
      </option>
    </select>

    <!-- Кнопка выдачи -->
    <button @click="loanBook" :disabled="!canLoan" class="btn">
      Выдать книгу
    </button>

    <!-- Список выданных книг -->
    <div v-if="loans.length > 0" class="table-wrapper">
      <h2>Список выданных книг</h2>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Дата выдачи</th>
            <th>Срок возврата</th>
            <th>Дата возврата</th>
            <th>Книга</th>
            <th>Читатель</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="loan in loans" :key="loan.id">
            <td>{{ loan.id }}</td>
            <td>{{ loan.loan_date }}</td>
            <td>{{ loan.due_date }}</td>
            <td>{{ loan.return_date || 'Не возвращена' }}</td>
            <td>{{ getBookTitle(loan.book) }}</td>
            <td>{{ getReaderName(loan.reader) }}</td>
            <td>
              <button
                v-if="!loan.return_date"
                @click="returnBook(loan.id)"
                class="btn return"
              >
                Вернуть
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Нет выданных книг</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const books = ref([])
const readers = ref([])
const loans = ref([])

const loan = ref({ book: '', reader: '' })

const loadBooks = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/book/')
    books.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки книг:', error)
  }
}

const loadReaders = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/reader/')
    readers.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки читателей:', error)
  }
}

const loadLoans = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/loan/')
    loans.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки списка займов:', error)
    alert('Не удалось загрузить список займов')
  }
}

const canLoan = computed(() => {
  const book = books.value.find(b => b.id === loan.value.book)
  return loan.value.book && loan.value.reader && book?.available_copies > 0
})

const loanBook = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/loan/', loan.value)
    alert('Книга выдана!')
    loan.value = { book: '', reader: '' }
    await loadBooks()
    await loadLoans()
  } catch (error) {
    console.error('Ошибка при выдаче:', error)
    alert('Ошибка при выдаче: ' + (error.response?.data?.detail || error.message))
  }
}

// Новая функция возврата книги
const returnBook = async (loanId) => {
  try {
    await axios.post(`http://127.0.0.1:8000/loan/${loanId}/return/`)
    alert('Книга возвращена!')
    await loadBooks()
    await loadLoans()
  } catch (error) {
    console.error('Ошибка при возврате:', error)
    alert('Ошибка при возврате: ' + (error.response?.data?.detail || error.message))
  }
}

const getBookTitle = (bookId) => {
  const book = books.value.find(b => b.id === bookId)
  return book ? book.title : 'Неизвестно'
}

const getReaderName = (readerId) => {
  const reader = readers.value.find(r => r.id === readerId)
  return reader ? `${reader.last_name} ${reader.first_name}` : 'Неизвестно'
}

onMounted(async () => {
  await loadBooks()
  await loadReaders()
  await loadLoans()
})
</script>


<style scoped>
.page h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
}



/* ==================== Кнопки ==================== */
.btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
  transition: transform 0.2s ease;
}

.btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.return {
  background: #1976d2;
  padding: 0.5rem 1rem;
}
</style>