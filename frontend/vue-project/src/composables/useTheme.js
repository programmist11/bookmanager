// src/composables/useTheme.js
import { ref, onMounted } from 'vue'

export function useTheme() {
  const isDark = ref(false)

  const applyTheme = () => {
    document.body.classList.toggle('dark', isDark.value)
    localStorage.setItem('darkMode', isDark.value)
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
  }

  onMounted(() => {
    isDark.value = localStorage.getItem('darkMode') === 'true'
    applyTheme()
  })

  return { isDark, toggleTheme }
}
