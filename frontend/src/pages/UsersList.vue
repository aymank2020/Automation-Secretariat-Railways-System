<template>
  <div>
    <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h3 class="text-lg font-bold text-gray-800">إدارة المستخدمين</h3>
        <button
          @click="showAddModal = true"
          class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          إضافة مستخدم
        </button>
      </div>
    </div>

    <!-- Users List -->
    <div class="bg-white rounded-xl shadow-sm">
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <div v-else-if="users.length === 0" class="p-8 text-center text-gray-500">
        لا يوجد مستخدمين
      </div>
      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="user in users"
          :key="user.id"
          class="p-6 flex items-center justify-between hover:bg-gray-50"
        >
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
              {{ user.full_name?.charAt(0) || user.username.charAt(0) }}
            </div>
            <div>
              <h4 class="font-semibold text-gray-800">{{ user.full_name || user.username }}</h4>
              <p class="text-sm text-gray-500">@{{ user.username }}</p>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <span
              :class="[
                'px-3 py-1 rounded-full text-sm',
                user.seclevel === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
              ]"
            >
              {{ user.seclevel === 'admin' ? 'مدير' : 'مستخدم' }}
            </span>
            <span v-if="!user.is_active" class="px-2 py-1 rounded text-xs bg-red-100 text-red-700">
              غير نشط
            </span>
            <button
              v-if="user.id !== authStore.user?.id"
              @click="handleDelete(user)"
              class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
        <h3 class="text-xl font-bold text-gray-800 mb-4">إضافة مستخدم جديد</h3>
        <form @submit.prevent="handleAddUser" class="space-y-4">
          <div>
            <label class="block text-gray-700 font-medium mb-2">اسم المستخدم *</label>
            <input
              v-model="newUser.username"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="أدخل اسم المستخدم"
              required
            />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-2">الاسم الكامل</label>
            <input
              v-model="newUser.full_name"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="الاسم الكامل"
            />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-2">كلمة المرور *</label>
            <input
              v-model="newUser.password"
              type="password"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="كلمة المرور"
              required
            />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-2">الصلاحية *</label>
            <select
              v-model="newUser.seclevel"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="user">مستخدم</option>
              <option value="admin">مدير</option>
            </select>
          </div>
          <div class="flex gap-2 pt-4">
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              <span v-if="loading">جاري الحفظ...</span>
              <span v-else>إضافة</span>
            </button>
            <button
              type="button"
              @click="showAddModal = false; resetForm()"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              إلغاء
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { userApi } from '@/services/api'

const authStore = useAuthStore()

const loading = ref(false)
const users = ref([])
const showAddModal = ref(false)

const newUser = ref({
  username: '',
  full_name: '',
  password: '',
  seclevel: 'user'
})

async function loadUsers() {
  loading.value = true
  try {
    const response = await userApi.getAll()
    users.value = response.data
  } catch (error) {
    console.error('Error loading users:', error)
  } finally {
    loading.value = false
  }
}

async function handleAddUser() {
  loading.value = true
  try {
    await userApi.create(newUser.value)
    showAddModal.value = false
    resetForm()
    loadUsers()
  } catch (error) {
    console.error('Error adding user:', error)
    alert('حدث خطأ أثناء إضافة المستخدم')
  } finally {
    loading.value = false
  }
}

async function handleDelete(user) {
  if (!confirm(`هل أنت متأكد من حذف المستخدم "${user.username}"؟`)) return

  try {
    await userApi.delete(user.id)
    loadUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    alert('حدث خطأ أثناء حذف المستخدم')
  }
}

function resetForm() {
  newUser.value = {
    username: '',
    full_name: '',
    password: '',
    seclevel: 'user'
  }
}

onMounted(() => {
  loadUsers()
})
</script>