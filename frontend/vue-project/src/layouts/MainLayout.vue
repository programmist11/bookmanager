<template>
  <div>
    <!-- HEADER НА ВСЮ ШИРИНУ -->
    <header class="header">
      <div class="header-content">
        <NavBar />

        <button @click="toggleTheme" class="toggle-theme">
          {{ isDark ? 'Светлая тема' : 'Темная тема' }}
        </button>
      </div>
    </header>

    <!-- ОСНОВНОЙ КОНТЕНТ -->
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
// import { useTheme } from '@/composables/useTheme'

// const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
/* === HEADER НА ВСЮ ШИРИНУ === */
.header {
  background: var(--header-bg);
  color: var(--header-text);
  padding: 1rem 0; /* вертикальные отступы */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* Внутренний контейнер для контента */
.header-content {
  max-width: 1280px; 
  margin: 0 auto;
  padding: 0 2rem; /* горизонтальные отступы */
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* NAVBAR внутри header */
.header-content nav {
  display: flex;
  gap: 1rem;
}

/* Кнопка переключения темы */
.toggle-theme {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background-color: #160101cc;
  color: #d1cccc;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}
.toggle-theme:hover {
  opacity: 0.85;
}

/* Основной контент */
.main {
  padding: 2rem;
}

/* === ТЁМНАЯ ТЕМА === */
body.dark .header {
  background: var(--header-bg);
  color: var(--header-text);
}
body.dark .toggle-theme {
  background-color: #6366f1;
  color: white;
}
</style>
