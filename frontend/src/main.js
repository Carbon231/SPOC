import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'
import Router from "vue-router";
Vue.config.productionTip = false

// new Vue({
//   render: h => h(App),
// }).$mount('#app')


Vue.use(ElementUI);
Vue.use(Router)

new Vue({
 el: '#app',
 router,
 render: h => h(App)
});


// // The Vue build version to load with the `import` command
// // (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import Vue from 'vue'
// import axios from 'axios'
// import ElementUI from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css'
// import App from './App'
// import router from './router'
// // import cookie from './util/cookie'
//
// Vue.use(ElementUI)
// Vue.config.productionTip = false
// Vue.prototype.$http = axios
// Vue.prototype.$url = 'http://127.0.0.1:8000/'
// // Vue.prototype.cookie = cookie
//
// /* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   components: { App },
//   template: '<App/>',
//   data: function () {
//     return {
//       isCollapsed: true
//     }
//   }
// })

