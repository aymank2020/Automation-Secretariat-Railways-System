<template>
  <div>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">إجمالي المراسلات</p>
            <p class="text-3xl font-bold text-gray-800 mt-2">{{ stats.total }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">المراسلات الواردة</p>
            <p class="text-3xl font-bold text-green-600 mt-2">{{ stats.incoming }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">المراسلات الصادرة</p>
            <p class="text-3xl font-bold text-orange-600 mt-2">{{ stats.outgoing }}</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">مستخدمو النظام</p>
            <p class="text-3xl font-bold text-purple-600 mt-2">{{ stats.users }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Documents -->
    <div class="bg-white rounded-xl shadow-sm">
      <div class="p-6 border-b border-gray-100">
        <h3 class="text-lg font-bold text-gray-800">آخر المراسلات</h3>
      </div>
      <div class="p-6">
        <div v-if="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        <div v-else-if="recentDocuments.length === 0" class="text-center py-8 text-gray-500">
          لا توجد مراسلات حديثة
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="doc in recentDocuments"
            :key="doc.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
            @click="$router.push(`/documents/${doc.id}`)"
          >
            <div class="flex items-center gap-4">
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  doc.doc_type === 'warid' ? 'bg-green-100' : 'bg-orange-100'
                ]"
              >
                <span class="font-bold" :class="doc.doc_type === 'warid' ? 'text-green-600' : 'text-orange-600'">
                  {{ doc.doc_type === 'warid' ? 'وارد' : 'صادر' }}
                </span>
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ doc.subject }}</p>
                <p class="text-sm text-gray-500">{{ doc.doc_number }}</p>
              </div>
            </div>
            <div class="text-left">
              <p class="text-sm text-gray-600">{{ formatDate(doc.date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
      <button
        @click="$router.push('/documents/new?doc_type=warid')"
        class="bg-green-600 text-white p-6 rounded-xl hover:bg-green-700 transition-colors text-right"
      >
        <h3 class="font-bold text-lg">إضافة مراسلة واردة</h3>
        <p class="text-green-100 mt-1">تسجيل مراسلة واردة جديدة</p>
      </button>
      <button
        @click="$router.push('/documents/new?doc_type=sadir')"
        class="bg-orange-600 text-white p-6 rounded-xl hover:bg-orange-700 transition-colors text-right"
      >
        <h3 class="font-bold text-lg">إضافة مراسلة صادرة</h3>
        <p class="text-orange-100 mt-1">تسجيل مراسلة صادرة جديدة</p>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { documentApi } from '@/services/api'

const loading = ref(true)
const recentDocuments = ref([])
const stats = ref({
  total: 0,
  incoming: 0,
  outgoing: 0,
  users: 0
})

async function loadDashboardData() {
  try {
    const docsResponse = await documentApi.getAll({ limit: 5 })
    recentDocuments.value = docsResponse.data

    // Load stats
    const allDocs = await documentApi.getAll({ limit: 1000 })
    const documents = allDocs.data
    stats.value.total = documents.length
    stats.value.incoming = documents.filter(d => d.doc_type === 'warid').length
    stats.value.outgoing = documents.filter(d => d.doc_type === 'sadir').length
  } catch (error) {
    console.error('Error loading dashboard:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-EG', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadDashboardData()
})
</script>