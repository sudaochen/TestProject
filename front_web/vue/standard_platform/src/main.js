import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import api from "./API/api"
import user from "./API/request"

Vue.config.productionTip = false
Vue.prototype.$api=api  //定义被调用的通信协议入口
Vue.prototype.$user=user

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
