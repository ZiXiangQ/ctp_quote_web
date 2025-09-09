import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { Quasar } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)
app.use(createPinia())
app.use(Quasar, { plugins: {} })
app.use(router)
app.mount('#app')
