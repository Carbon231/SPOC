import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import Router from "vue-router"
import cookie from './util/cookie'

Vue.config.productionTip = false
Vue.prototype.$http = axios
Vue.prototype.$url = 'http://127.0.0.1:8000/'
Vue.prototype.cookie = cookie


Vue.use(ElementUI);
Vue.use(Router)

new Vue({
 el: '#app',
 router,
 render: h => h(App)
});

