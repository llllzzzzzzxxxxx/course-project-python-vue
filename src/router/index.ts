import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
      path: '/',
      redirect: '/downloadHistory'
    },
    {
      path: '/downloadHistory',
      component: () => import('../views/DownloadHistory.vue')
    },
    {
      path: '/Search',
      component: () => import('../views/Search.vue')
    }
  ],
  scrollBehavior(){
    return {
        left: 0,
        top: 0
    }
}
})

export default router;