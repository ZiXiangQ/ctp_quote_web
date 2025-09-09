import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/quotes' },
  { path: '/quotes', name: 'quotes', component: () => import('../pages/Quotes.vue') },
  { path: '/subscribe', name: 'subscribe', component: () => import('../pages/Subscribe.vue') },
  { path: '/settings', name: 'settings', component: () => import('../pages/Settings.vue') },
  { path: '/about', name: 'about', component: () => import('../pages/About.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
