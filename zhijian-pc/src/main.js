import Vue from 'vue'
import App from './App.vue'
import router from './router'
import iView from 'iview';
import '@/utils/requests'
import requestURL from '@/router/urlPath'
import 'iview/dist/styles/iview.css';
import '@/assets/css/common.less'
import '@/assets/css/common.css'
import * as qiniu from 'qiniu-js'
import { debug } from 'util';
Vue.use(qiniu);
Vue.use(iView);
Vue.config.productionTip = false
Vue.prototype.PATH = requestURL
    // Vue.prototype.URL = 'https://bjzhijian.max-tv.net.cn/api/tv1_0/'
Vue.prototype.URL = 'https://bjzhijian.max-tv.net.cn/api/tv1_0/'
Vue.mixin({
    beforeCreate: function() {
        let that = this;
        if (!sessionStorage.getItem('userName')) {
            that.$router.push({
                name: 'login'
            })
        }
    }
})
new Vue({
        router,
        render: h => h(App)
    }).$mount('#app')
    // 路由守卫判断是否登录
router.beforeEach((to, from, next) => {

    if (to.meta.requireAuth) { //如果需要跳转 ，往下走（1）
        let userName = sessionStorage.getItem('userName');
        if (userName) { //判断是否登录过，如果有登陆过，说明有token,或者token未过期，可以跳过登录（2）
            if (to.path === '/') { //判断下一个路由是否为要验证的路由（3）
                next('/index'); // 如果是直接跳到首页，
            } else { //如果该路由不需要验证，那么直接往后走
                next();
            }
        } else {
            next('/');
            console.log('没有'); //如果没有登陆过，或者token 过期， 那么跳转到登录页
        }
    } else { //不需要跳转，直接往下走
        next();
    }
})