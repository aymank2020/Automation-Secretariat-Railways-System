import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/pages/Dashboard.vue')
      },
      {
        path: 'documents',
        name: 'documents',
        component: () => import('@/pages/DocumentsList.vue')
      },
      {
        path: 'documents/new',
        name: 'document-new',
        component: () => import('@/pages/DocumentForm.vue')
      },
      {
        path: 'documents/:id/edit',
        name: 'document-edit',
        component: () => import('@/pages/DocumentForm.vue')
      },
      {
        path: 'documents/:id',
        name: 'document-detail',
        component: () => import('@/pages/DocumentDetails.vue')
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('@/pages/UsersList.vue'),
        meta: { requiresAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = authStore.token

  if (to.meta.guest && token) {
    next('/dashboard')
  } else if (to.meta.requiresAdmin && authStore.user?.seclevel !== 'admin') {
    next('/dashboard')
  } else if (!to.meta.guest && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router