<template>
  <div>
    <div class="bg-white rounded-xl shadow-sm p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-6">
        {{ isEdit ? 'تعديل المراسلة' : 'إضافة مراسلة جديدة' }}
        <span v-if="form.doc_type" class="mr-2" :class="form.doc_type === 'warid' ? 'text-green-600' : 'text-orange-600'">
          ({{ form.doc_type === 'warid' ? 'وارد' : 'صادر' }})
        </span>
      </h2>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Document Type -->
        <div v-if="!isEdit" class="grid grid-cols-2 gap-4">
          <button
            type="button"
            @click="form.doc_type = 'warid'"
            :class="[
              'p-6 rounded-xl border-2 transition-all',
              form.doc_type === 'warid' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-green-300'
            ]"
          >
            <div class="text-center">
              <svg class="w-12 h-12 mx-auto mb-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
              </svg>
              <span class="font-bold text-lg">مراسلة واردة</span>
            </div>
          </button>
          <button
            type="button"
            @click="form.doc_type = 'sadir'"
            :class="[
              'p-6 rounded-xl border-2 transition-all',
              form.doc_type === 'sadir' ? 'border-orange-500 bg-orange-50' : 'border-gray-200 hover:border-orange-300'
            ]"
          >
            <div class="text-center">
              <svg class="w-12 h-12 mx-auto mb-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
              </svg>
              <span class="font-bold text-lg">مراسلة صادرة</span>
            </div>
          </button>
        </div>

        <!-- Basic Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-2">رقم المراسلة *</label>
            <input
              v-model="form.doc_number"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="أدخل رقم المراسلة"
              required
            />
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-2">التاريخ *</label>
            <input
              v-model="form.date"
              type="date"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">الموضوع *</label>
          <textarea
            v-model="form.subject"
            rows="2"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="أدخل موضوع المراسلة"
            required
          ></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-2">المصدر <span v-if="form.doc_type === 'warid'">*</span></label>
            <input
              v-model="form.source"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="form.doc_type === 'warid' ? 'من جاءت المراسلة؟' : 'اختياري'"
            />
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-2">الوجهة <span v-if="form.doc_type === 'sadir'">*</span></label>
            <input
              v-model="form.destination"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              :placeholder="form.doc_type === 'sadir' ? 'إلى أين؟' : 'اختياري'"
            />
          </div>
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">المحتوى</label>
          <textarea
            v-model="form.content"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="تفاصيل المحتوى..."
          ></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-2">الأولوية</label>
            <select
              v-model="form.priority"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="low">عادي</option>
              <option value="normal">متوسط</option>
              <option value="high">عالي</option>
              <option value="urgent">عاجل</option>
            </select>
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-2">الحالة</label>
            <select
              v-model="form.status"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="new">جديد</option>
              <option value="in_progress">قيد المعالجة</option>
              <option value="completed">مكتمل</option>
              <option value="archived">مؤرشف</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">ملاحظات</label>
          <textarea
            v-model="form.notes"
            rows="2"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="ملاحظات إضافية..."
          ></textarea>
        </div>

        <!-- File Upload -->
        <div>
          <label class="block text-gray-700 font-medium mb-2">ملف مرفق</label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input
              ref="fileInput"
              type="file"
              @change="handleFileChange"
              accept=".pdf,.jpg,.jpeg,.png"
              class="hidden"
            />
            <button
              type="button"
              @click="$refs.fileInput.click()"
              class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
            >
              اختيار ملف
            </button>
            <p class="text-sm text-gray-500 mt-2">PDF, JPG, PNG (حد أقصى 5MB)</p>
            <p v-if="selectedFile" class="text-sm text-blue-600 mt-2">{{ selectedFile.name }}</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            <span v-if="loading">جاري الحفظ...</span>
            <span v-else>{{ isEdit ? 'حفظ التعديلات' : 'إضافة المراسلة' }}</span>
          </button>
          <button
            type="button"
            @click="$router.back()"
            class="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            إلغاء
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { documentApi } from '@/services/api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const docId = computed(() => route.params.id)

const loading = ref(false)
const selectedFile = ref(null)
const fileInput = ref(null)

const form = ref({
  doc_type: route.query.doc_type || 'warid',
  doc_number: '',
  subject: '',
  source: '',
  destination: '',
  date: new Date().toISOString().split('T')[0],
  content: '',
  priority: 'normal',
  status: 'new',
  notes: ''
})

async function loadData() {
  if (!isEdit.value) return

  loading.value = true
  try {
    const response = await documentApi.getById(docId.value)
    const doc = response.data

    form.value = {
      doc_type: doc.doc_type,
      doc_number: doc.doc_number,
      subject: doc.subject,
      source: doc.source || '',
      destination: doc.destination || '',
      date: doc.date.split('T')[0],
      content: doc.content || '',
      priority: doc.priority,
      status: doc.status,
      notes: doc.notes || ''
    }
  } catch (error) {
    console.error('Error loading document:', error)
  } finally {
    loading.value = false
  }
}

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('حجم الملف كبير جداً. الحد الأقصى 5MB')
      return
    }
    selectedFile.value = file
  }
}

async function handleSubmit() {
  loading.value = true

  try {
    const formData = new FormData()
    Object.keys(form.value).forEach(key => {
      formData.append(key, form.value[key])
    })

    if (selectedFile.value) {
      formData.append('file', selectedFile.value)
    }

    if (isEdit.value) {
      await documentApi.update(docId.value, form.value)
    } else {
      await documentApi.create(form.value)
    }

    router.push('/documents')
  } catch (error) {
    console.error('Error saving document:', error)
    alert('حدث خطأ أثناء الحفظ. حاول مرة أخرى.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>