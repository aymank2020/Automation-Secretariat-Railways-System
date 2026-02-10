<template>
  <div
    :class="[
      'fixed top-0 right-0 h-full w-64 bg-slate-800 text-white shadow-lg transition-transform duration-300 z-40',
      isOpen ? 'translate-x-0' : 'translate-x-full', 'lg:translate-x-0'
    ]"
  >
    <div class="p-6">
      <h1 class="text-xl font-bold mb-6">نظام المراسلات</h1>
      <p class="text-sm text-gray-300 mb-6">السكك الحديدية</p>

      <nav class="space-y-2">
        <router-link
          to="/dashboard"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-700 transition-colors"
          active-class="bg-slate-700"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
          </svg>
          لوحة التحكم
        </router-link>

        <router-link
          to="/documents"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-700 transition-colors"
          active-class="bg-slate-700"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          المراسلات
        </router-link>

        <router-link
          v-if="authStore.isAdmin"
          to="/users"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-700 transition-colors"
          active-class="bg-slate-700"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
          </svg>
          المستخدمين
        </router-link>
      </nav>
    </div>

    <div class="absolute bottom-0 right-0 left-0 p-6 border-t border-slate-700">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center font-bold">
          {{ authStore.user?.full_name?.charAt(0) || 'A' }}
        </div>
        <div>
          <p class="font-medium text-sm">{{ authStore.user?.full_name || 'مستخدم' }}</p>
          <p class="text-xs text-gray-300">{{ authStore.user?.seclevel === 'admin' ? 'مدير' : 'مستخدم' }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Overlay for mobile -->
  <div
    v-if="isOpen"
    @click="$emit('close')"
    class="fixed inset-0 bg-black/50 z-30 lg:hidden"
  ></div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const authStore = useAuthStore()
</script>