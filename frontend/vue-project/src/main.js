import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Подключаем CSS с темами
import './assets/styles/main.css'


const app = createApp(App)
app.use(router)
app.mount('#app')


const isDark = localStorage.getItem('darkMode') === 'true'
if (isDark) {
  document.body.classList.add('dark')
}

// Функция для переключения темы (можно вызывать из любого компонента)
app.config.globalProperties.$toggleTheme = () => {
  document.body.classList.toggle('dark')
  const dark = document.body.classList.contains('dark')
  localStorage.setItem('darkMode', dark)
}
