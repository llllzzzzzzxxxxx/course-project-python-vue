import '@/style/reset.scss'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import App from './App.vue'
// import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
