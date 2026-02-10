<template>
  <header class="bg-white shadow-sm">
    <div class="flex justify-between items-center px-6 py-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">{{ pageTitle }}</h2>
        <p v-if="pageSubtitle" class="text-gray-500">{{ pageSubtitle }}</p>
      </div>

      <div class="flex items-center gap-4">
        <button
          @click="$emit('logout')"
          class="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
          تسجيل خروج
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageTitle = computed(() => {
  const titles = {
    'home': 'لوحة التحكم',
    'documents': 'المراسلات',
    'document-new': 'إضافة مراسلة جديدة',
    'document-edit': 'تعديل المراسلة',
    'document-detail': 'تفاصيل المراسلة',
    'users': 'المستخدمين'
  }
  return titles[route.name] || 'النظام'
})

const pageSubtitle = computed(() => {
  const subtitles = {
    'documents': 'عرض وإدارة المراسلات الواردة والصادرة',
    'users': 'إدارة صلاحيات المستخدمين'
  }
  return subtitles[route.name] || ''
})

defineEmits(['logout'])
</script>