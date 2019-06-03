// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import App from './App'
import router from './router'
import '@/utils/requests'
import requestURL from '@/router/urlpath'
import iView from 'iview'
import  VueQuillEditor from 'vue-quill-editor'
// import { Vue, iView, router } from '../commentjs/vendor.dll'
import 'iview/dist/styles/iview.css'
import '@/assets/iconfont/iconfont.css'
import '@/assets/css/global.css'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'


Vue.use(iView)
Vue.use(VueQuillEditor)

Vue.config.productionTip = false
Vue.prototype.PATH = requestURL


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    'App': ()=> import('./App')
  },
  template: '<App/>'
})
