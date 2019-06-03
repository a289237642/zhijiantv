import Vue from 'vue'
import Router from 'vue-router'
import path from './routePath'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: path.login
    },
    {
      path: '/home',
      name: 'home',
      component: path.home,
      children: [
        {
          //首页
          path: '/index',
          name: 'index',
          component: path.index
        },
        {
          //活动列表
          path: '/ActivityList',
          name: 'ActivityList',
          component: path.ActivityList
        },
        {
          //爆料列表
          path: '/tipoffList',
          name: 'tipoffList',
          component: path.tipoffList
        },
        {
          //大公司头条’
          path: '/CompanyHeadline',
          name: 'CompanyHeadline',
          component: path.CompanyHeadline
        },
        {
          //爆料库
          path: '/tipoffLibrary',
          name: 'tipoffLibrary',
          component: path.tipoffLibrary
        },
        {
          //爆料类型管理
          path: '/tipoffManagement',
          name: 'tipoffManagement',
          component: path.tipoffManagement
        },
        {
          //icon管理
          path: '/iconManagement',
          name: 'iconManagement',
          component: path.iconManagement
        },
        {
          //签到海报管理
          path: '/signManagement',
          name: 'signManagement',
          component: path.signManagement
        },
        {
          //用户列表
          path: '/userList',
          name: 'userList',
          component: path.userList
        },
        //banner管理
        {
          path: '/bannerManagement',
          name: 'bannerManagement',
          component: path.bannerManagement
        },
        //学堂管理
        {
          path: '/schoolManagement',
          name: 'schoolManagement',
          component: path.schoolManagement
        },
        //公众号库
        {
          path: '/vipcnLibrary',
          name: 'vipcnLibrary',
          component: path.vipcnLibrary
        },
        //公众号列表
        {
          path: '/vipcnList',
          name: 'vipcnList',
          component: path.vipcnList
        },
        {
          //修改密码
          path: '/ChangePassword',
          name: 'ChangePassword',
          component: path.ChangePassword
        },
        {
          //课程管理
          path: '/lessonManagement',
          name: 'lessonManagement',
          component: path.lessonManagement
        },
        {
          //课程音频
          path: '/lessonAudio',
          name: 'lessonAudio',
          component: path.lessonAudio
        },
        {
          //免费听
          path: '/freeListen',
          name: 'freeListen',
          component: path.freeListen
        },
        {
          //商学院
          path: '/business',
          name: 'business',
          component: path.business
        },
        {
          //类型管理
          path: '/typeManagement',
          name: 'typeManagement',
          component: path.typeManagement
        },
        {
          //头像库
          path: '/headImage',
          name: 'headImage',
          component: path.headImage
        },
        {
          //头像库
          path: '/lessonLibray',
          name: 'lessonLibray',
          component: path.lessonLibray
        },
        {
          //商品列表
          path: '/goodsList',
          name: 'goodsList',
          component: path.goodsList
        },
        {
          //添加商品
          path: '/addGoods',
          name: 'addGoods',
          component: path.addGoods
        },
        {
          //申请人列表
          path: '/applicationLists',
          name: 'applicationLists',
          component: path.applicationLists
        },
        {
          //广告管理
          path: '/advList',
          name: 'advList',
          component: path.advList
        },
        {
          //渠道管理
          path: '/channelList',
          name: 'channelList',
          component: path.channelList
        },
        {
          //数据概览
          path: '/dataOverview',
          name: 'dataOverview',
          component: path.dataOverview
        },
        {
          //渠道数据详情
          path: '/spreadDetail',
          name: 'spreadDetail',
          component: path.spreadDetail
        },
        {
          //订单管理
          path: '/orderList',
          name: 'orderList',
          component: path.orderList
        },
        {
          //订单管理
          path: '/orderDetail',
          name: 'orderDetail',
          component: path.orderDetail
        },
        {
          //文章标签管理
          path: '/keywordsManagement',
          name: 'keywordsManagement',
          component: path.keywordsManagement
        },
        {
          //文章敏感词管理
          path: '/sensitivewordsManagement',
          name: 'sensitivewordsManagement',
          component: path.sensitivewordsManagement
        }
      ]
    }
  ]
})
