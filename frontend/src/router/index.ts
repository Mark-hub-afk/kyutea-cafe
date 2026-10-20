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
      component: MenuView
    },
    {
      path: '/admin',
      redirect: '/admin/orders'
    },
    {
      path: '/admin/orders',
      name: 'admin-orders',
      component: AdminPanel
    },
    {
      path: '/admin/inventory',
      name: 'admin-inventory',
      component: AdminPanel
    },
    {
      path: '/admin/addons',
      name: 'admin-addons',
      component: AdminPanel
    },
    {
      path: '/admin/approvals',
      name: 'admin-approvals',
      component: AdminPanel
    },
    {
      path: '/admin/resets',
      name: 'admin-resets',
      component: AdminPanel
    }
  ],
})

export default router