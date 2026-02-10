<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Mobile menu button -->
    <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden p-4 fixed top-0 right-0 z-50">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
      </svg>
    </button>

    <!-- Sidebar -->
    <Sidebar :isOpen="sidebarOpen" @close="sidebarOpen = false" />

    <!-- Main content -->
    <div :class="['lg:mr-64 transition-all duration-300', sidebarOpen ? 'mr-64' : 'mr-0']">
      <Header @logout="handleLogout" />

      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const router = useRouter()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>