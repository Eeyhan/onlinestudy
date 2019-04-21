// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'



// elementUI 导入
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 调用插件
Vue.use(ElementUI);

// 导入vuex
import store from '../src/store'

// 导入全局css
import '../static/global/global.css'

// 导入极验js
import '../static/global/gt.js'


import '../static/global/axios.js'

// 导入api接口函数
import * as api from './RestfulApi/api.js'
Vue.prototype.$http = api

// 全局守卫
router.beforeEach((to, form, next) => {
  if (localStorage.getItem('access_token')) {
    let user = {
      access_token: localStorage.getItem('access_token'),
      username: localStorage.getItem('username'),
      avatar: localStorage.getItem('avatar'),
      shop_cart_num: localStorage.getItem('shop_cart_num'),
      balance:localStorage.getItem('balance')
    }
    store.dispatch('getUserInfo', user)
  }
  next()
})


// Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
