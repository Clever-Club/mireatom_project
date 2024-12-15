import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import LoginView from '@/views/LoginView.vue'
import FormulaInputView from '@/views/FormulaInputView.vue'
import FormulaAnalysisView from '@/views/FormulaAnalysisView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/formula-input',
      name: 'formula-input',
      component: FormulaInputView,
    },
    {
      path: '/formula-analysis',
      name: 'formula-analysis',
      component: FormulaAnalysisView,
    },
  ],
})

export default router
