<template>
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
          <td><img v-if="book.cover" :src="book.cover" class="cover" /></td>
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
            <button @click="$emit('editBook', book)" class="btn edit">✏️</button>
            <button @click="$emit('deleteBook', book.id)" class="btn delete">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="empty"><p>Книг пока нет</p></div>
</template>

<script setup>
defineProps({ books: Array })
const emit = defineEmits(['editBook', 'deleteBook'])
</script>
