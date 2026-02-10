<template>
  <div>
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else-if="document" class="space-y-6">
      <!-- Document Header -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex justify-between items-start mb-4">
          <div class="flex items-center gap-3">
            <span
              :class="[
                'px-4 py-2 rounded-full font-bold text-lg',
                document.doc_type === 'warid' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
              ]"
            >
              {{ document.doc_type === 'warid' ? 'مراسلة واردة' : 'مراسلة صادرة' }}
            </span>
            <span class="px-3 py-1 rounded text-sm" :class="getPriorityClass(document.priority)">
              {{ getPriorityText(document.priority) }}
            </span>
          </div>
          <div class="flex gap-2">
            <button
              @click="$router.push(`/documents/${document.id}/edit`)"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              تعديل
            </button>
            <button
              v-if="authStore.isAdmin"
              @click="handleDelete"
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              حذف
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-500">رقم المراسلة:</span>
            <span class="font-medium mr-2">{{ document.doc_number }}</span>
          </div>
          <div>
            <span class="text-gray-500">التاريخ:</span>
            <span class="font-medium mr-2">{{ formatDate(document.date) }}</span>
          </div>
          <div>
            <span class="text-gray-500">المصدر:</span>
            <span class="font-medium mr-2">{{ document.source || 'غير محدد' }}</span>
          </div>
          <div>
            <span class="text-gray-500">الوجهة:</span>
            <span class="font-medium mr-2">{{ document.destination || 'غير محدد' }}</span>
          </div>
          <div>
            <span class="text-gray-500">الحالة:</span>
            <span class="px-2 py-1 rounded text-xs mr-2" :class="getStatusClass(document.status)">
              {{ getStatusText(document.status) }}
            </span>
          </div>
          <div>
            <span class="text-gray-500">تم الإنشاء:</span>
            <span class="font-medium mr-2">{{ formatDate(document.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Subject -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="font-bold text-gray-800 mb-2">الموضوع</h3>
        <p class="text-lg">{{ document.subject }}</p>
      </div>

      <!-- Content -->
      <div v-if="document.content" class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="font-bold text-gray-800 mb-4">المحتوى</h3>
        <p class="text-gray-700 whitespace-pre-wrap">{{ document.content }}</p>
      </div>

      <!-- Notes -->
      <div v-if="document.notes" class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="font-bold text-gray-800 mb-4">ملاحظات</h3>
        <p class="text-gray-600">{{ document.notes }}</p>
      </div>

      <!-- File Attachment -->
      <div v-if="document.file_name" class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="font-bold text-gray-800 mb-4">الملف المرفق</h3>
        <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <div>
            <p class="font-medium text-gray-800">{{ document.file_name }}</p>
            <p class="text-sm text-gray-500">{{ document.file_type || 'ملف مرفق' }}</p>
          </div>
        </div>
      </div>

      <!-- History -->
      <div v-if="history.length > 0" class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="font-bold text-gray-800 mb-4">سجل التعديلات</h3>
        <div class="space-y-4">
          <div
            v-for="(item, index) in history"
            :key="item.id"
            class="flex gap-4 pb-4"
            :class="{ 'border-b border-gray-100': index < history.length - 1 }"
          >
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-blue-600 font-bold">{{ item.user?.full_name?.charAt(0) || 'U' }}</span>
            </div>
            <div class="flex-1">
              <div class="flex justify-between items-start">
                <p class="font-medium text-gray-800">{{ getActionText(item.action) }}</p>
                <span class="text-sm text-gray-500">{{ formatDate(item.action_at) }}</span>
              </div>
              <p class="text-sm text-gray-600 mr-8">{{ item.user?.full_name || 'مستخدم' }}</p>
              <p v-if="item.new_value" class="text-sm text-gray-500 mr-8 mt-1">{{ item.new_value }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm p-8 text-center text-gray-500">
      المراسلة غير موجودة
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { documentApi } from '@/services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const document = ref(null)
const history = ref([])

async function loadData() {
  loading.value = true
  try {
    const [docResponse, historyResponse] = await Promise.all([
      documentApi.getById(route.params.id),
      documentApi.getHistory(route.params.id)
    ])
    document.value = docResponse.data
    history.value = historyResponse.data
  } catch (error) {
    console.error('Error loading document:', error)
    router.push('/documents')
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!confirm('هل أنت متأكد من حذف هذه المراسلة؟')) return

  try {
    await documentApi.delete(route.params.id)
    router.push('/documents')
  } catch (error) {
    console.error('Error deleting document:', error)
    alert('حدث خطأ أثناء الحذف')
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-EG', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
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

function getStatusClass(status) {
  const classes = {
    new: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-yellow-100 text-yellow-700',
    completed: 'bg-green-100 text-green-700',
    archived: 'bg-gray-100 text-gray-700'
  }
  return classes[status] || classes.new
}

function getStatusText(status) {
  const texts = {
    new: 'جديد',
    in_progress: 'قيد المعالجة',
    completed: 'مكتمل',
    archived: 'مؤرشف'
  }
  return texts[status] || 'جديد'
}

function getActionText(action) {
  const texts = {
    created: 'تم الإنشاء',
    updated: 'تم التعديل',
    status_changed: 'تغيير الحالة',
    deleted: 'تم الحذف'
  }
  return texts[action] || action
}

onMounted(() => {
  loadData()
})
</script>