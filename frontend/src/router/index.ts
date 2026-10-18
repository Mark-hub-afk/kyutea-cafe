import { createRouter, createWebHistory } from 'vue-router'
import MenuView from '@/components/MenuView.vue'
import AdminPanel from '@/components/AdminPanel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MenuView
    },
    {
      path: '/add-ons',
      name: 'add-ons',
      // If you created an AddOnsView component, import it and map it here,
      // or map it to MenuView / a dedicated section if managed inline
      component: MenuView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel
    }
  ],
})

export default router