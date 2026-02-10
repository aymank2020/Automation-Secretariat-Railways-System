<template>
  <div>
    <!-- Tabs and Actions -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <!-- Tabs -->
        <div class="flex gap-2">
          <button
            @click="filter = 'all'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            الكل
          </button>
          <button
            @click="filter = 'warid'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              filter === 'warid' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            واردة
          </button>
          <button
            @click="filter = 'sadir'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              filter === 'sadir' ? 'bg-orange-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            صادرة
          </button>
        </div>

        <button
          @click="$router.push('/documents/new')"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          إضافة مراسلة
        </button>
      </div>

      <!-- Search -->
      <div class="mt-4">
        <input
          v-model="searchTerm"
          @input="handleSearch"
          type="text"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          placeholder="بحث في الموضوع، الرقم، المصدر، أو الوجهة..."
        />
      </div>
    </div>

    <!-- Documents List -->
    <div class="bg-white rounded-xl shadow-sm">
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="filteredDocuments.length === 0" class="p-8 text-center text-gray-500">
        لا توجد مراسلات
      </div>
      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="doc in filteredDocuments"
          :key="doc.id"
          class="p-6 hover:bg-gray-50 transition-colors cursor-pointer"
          @click="$router.push(`/documents/${doc.id}`)"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-sm font-medium',
                    doc.doc_type === 'warid' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
                  ]"
                >
                  {{ doc.doc_type === 'warid' ? 'وارد' : 'صادر' }}
                </span>
                <span class="text-gray-500">{{ doc.doc_number }}</span>
                <span class="px-2 py-1 rounded text-xs" :class="getPriorityClass(doc.priority)">
                  {{ getPriorityText(doc.priority) }}
                </span>
              </div>
              <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ doc.subject }}</h3>
              <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                <span v-if="doc.source">📥 من: {{ doc.source }}</span>
                <span v-if="doc.destination">📤 إلى: {{ doc.destination }}</span>
                <v>📅 {{ formatDate(doc.date) }}</v>
              </div>
            </div>
            <div v-if="doc.file_name" class="text-left">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { documentApi } from '@/services/api'

const loading = ref(true)
const documents = ref([])
const filter = ref('all')
const searchTerm = ref('')
let searchTimeout = null

const filteredDocuments = computed(() => {
  let result = documents.value

  if (filter.value !== 'all') {
    result = result.filter(d => d.doc_type === filter.value)
  }

  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(d =>
      d.subject?.toLowerCase().includes(term) ||
      d.doc_number?.toLowerCase().includes(term) ||
      d.source?.toLowerCase().includes(term) ||
      d.destination?.toLowerCase().includes(term)
    )
  }

  return result
})

async function loadDocuments() {
  loading.value = true
  try {
    const response = await documentApi.getAll({ limit: 100 })
    documents.value = response.data
  } catch (error) {
    console.error('Error loading documents:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  // Debounce search
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    // Search is handled by computed property
  }, 300)
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-EG')
}

function getPriorityClass(priority) {
  const classes = {
    low: 'bg-gray-100 text-gray-700',
    normal: 'bg-blue-100 text-blue-700',
    high: 'bg-yellow-100 text-yellow-700',
    urgent: 'bg-red-100 text-red-700'
  }
  return classes[priority] || classes.normal
}

function getPriorityText(priority) {
  const texts = {
    low: 'عادي',
    normal: 'متوسط',
    high: 'عالي',
    urgent: 'عاجل'
  }
  return texts[priority] || 'متوسط'
}

onMounted(() => {
  loadDocuments()
})
</script>