<!-- src/App.vue -->
<template>
  <div>
    <header class="header">
      <h1>📚 Библиотека</h1>
      <nav>
        <router-link to="/">Главная</router-link> |
        <router-link to="/books">Книги</router-link> |
        <router-link to="/readers">Читатели</router-link> |
        <router-link to="/loan">Выдать книгу</router-link> |
        <router-link to="/locations">Библиотеки</router-link>
      </nav>
    </header>

    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.header {
  background: #42b983;
  color: white;
  padding: 1rem;
  text-align: center;
}
.header a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
.main {
  padding: 2rem;
}
</style>
