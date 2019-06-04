import Vue from 'vue'
import Router from 'vue-router'
import path from '@/router/routePath'
// import Home from './views/Home.vue'
Vue.use(Router)

export default new Router({
    mode: 'history',
    // base: process.env.BASE_URL,
    routes: [{
            path: '/',
            name: 'login',
            component: path.login
        },
        {
            path: '/home',
            name: 'home',
            component: path.home,
            meta: { requireAuth: true },
            children: [{
                    //分类管理
                    path: '/classifyManagement',
                    name: 'classifyManagement',
                    meta: { requireAuth: true },
                    component: path.classifyManagement
                },
                {
                    //分类管理
                    path: '/uploadVideo',
                    name: 'uploadVideo',
                    meta: { requireAuth: true },
                    component: path.uploadVideo
                }
            ]
        },
    ]
})