<template>
  <div class="home">
    <h1>Добро пожаловать в библиотеку</h1>
    <p class="subtitle">Найдите свою следующую любимую книгу</p>
    <router-link to="/books" class="btn main-btn">Перейти к каталогу</router-link>

    <section v-if="featuredBooks.length" class="featured">
      <h2>Рекомендуем</h2>
      <div class="books-grid">
        <div v-for="book in featuredBooks" :key="book.id" class="book-card">
          <img :src="book.cover || 'https://via.placeholder.com/150'" :alt="book.title" class="cover" />
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">Автор: {{ book.author }}</p>
          <router-link :to="`/books/${book.id}`" class="link">Подробнее</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const featuredBooks = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/book/');
    featuredBooks.value = response.data.slice(0, 3); // первые 3 книги
  } catch (error) {
    console.error('Ошибка загрузки книг:', error);
  }
});
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.subtitle {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 1.5rem;
}

.btn.main-btn {
  display: inline-block;
  margin: 1rem 0 2rem;
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: 0.3s ease;
}

.btn.main-btn:hover {
  background-color: #36946e;
  transform: translateY(-2px);
}

.featured {
  margin-top: 2rem;
}

.books-grid {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.book-card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 1rem;
  width: 250px; /* увеличена ширина */
  text-align: left;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.cover {
  width: 100%;
  height: auto;
  max-height: 300px; /* ограничение сверху */
  object-fit: contain;
  border-radius: 8px;
}

.book-title {
  font-size: 1.1rem;
  margin: 0.6rem 0 0.2rem;
  color: #333;
}

.book-author {
  font-size: 0.9rem;
  color: #777;
}

.link {
  display: inline-block;
  margin-top: 0.5rem;
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
  transition: 0.2s ease;
}

.link:hover {
  text-decoration: underline;
  color: #36946e;
}

/* Адаптивность */
@media (max-width: 900px) {
  .book-card {
    width: 220px;
  }

  .cover {
    height: 220px;
  }
}

@media (max-width: 600px) {
  .books-grid {
    flex-direction: column;
    align-items: center;
  }

  .book-card {
    width: 90%;
  }

  .cover {
    height: 200px;
  }
}
</style>
