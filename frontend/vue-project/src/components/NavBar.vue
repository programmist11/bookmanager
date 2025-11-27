<template>
  <nav class="nav">
    <router-link
      v-for="item in menu"
      :key="item.to"
      :to="item.to"
      class="nav-link"
    >
      {{ item.label }}
    </router-link>
  </nav>
</template>

<script setup>
const menu = [
  { label: 'Главная', to: '/' },
  { label: 'Книги', to: '/books' },
  { label: 'Читатели', to: '/readers' },
  { label: 'Выдать книгу', to: '/loan' },
  { label: 'Библиотеки', to: '/locations' },
]
</script>
<!--  
<style scoped>
.nav {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap; /* чтобы элементы переносились на маленьких экранах */
  font-weight: bold;
}

.nav-link {
  text-decoration: none;
  color: var(--header-text); /* берём цвет текста из темы */
  padding: 4px 8px;
  border-radius: 6px;
  transition: 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2); /* легкий ховер эффект */
}

/* Адаптивность для маленьких экранов */
@media (max-width: 600px) {
  .nav {
    justify-content: center;
    gap: 0.5rem;
  }
  .nav-link {
    font-size: 0.9rem;
    padding: 3px 6px;
  }
}
</style>


!-->