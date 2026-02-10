<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">نظام إدارة المراسلات</h1>
        <p class="text-gray-500 mt-2">السكك الحديدية</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-gray-700 font-medium mb-2">اسم المستخدم</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="أدخل اسم المستخدم"
            required
          />
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">كلمة المرور</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="أدخل كلمة المرور"
            required
          />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          <span v-if="loading">جاري تسجيل الدخول...</span>
          <span v-else>تسجيل الدخول</span>
        </button>
      </form>

      <div class="mt-6 text-center text-sm text-gray-500">
        <p>بيانات الدخول الافتراضية:</p>
        <p class="mt-1"><strong>مدير:</strong> admin / admin123</p>
        <p><strong>مستخدم:</strong> user / user123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(form.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = 'اسم المستخدم أو كلمة المرور غير صحيحة'
  } finally {
    loading.value = false
  }
}
</script>