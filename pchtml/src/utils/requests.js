import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'
import router from '@/router/index'
import { LoadingBar, Message, Notice, Modal } from 'iview'

Vue.use(Router)

new Vue({ router })

LoadingBar.config({
    color: '#44f9e5',
    failedColor: '#dc4a51',
    height: 2
})

Message.config({
    top: 80,
    duration: 3
})

const arg = axios.create({
    timeout: 60000
})


//网络监测
if (!navigator.onLine) {
    Notice.destroy()
    Notice.error({
        title: '提示',
        desc: '无网络连接'
    })
}
const EventUtil = {
    addHandler: function (element, type, handler) {
        if (element.addEventListener) {
            element.addEventListener(type, handler, false)
        } else if (element.attachEvent) {
            element.attachEvent("on" + type, handler)
        } else {
            element["on" + type] = handler
        }
    }
}
EventUtil.addHandler(window, "online", () => {
    Notice.destroy()
    Notice.success({
        title: '提示',
        desc: '已连接到网络'
    })
})
EventUtil.addHandler(window, "offline", () => {
    Notice.destroy()
    Notice.error({
        title: '提示',
        desc: '网络连接已断开'
    })
})

//防止重复提交ajax
let pending = []
let flagUrl
let CancelToken = axios.CancelToken
let removePending = (config, f) => {
    // console.log(config,'config')
    if(config!=undefined){
        flagUrl = config.url + '&' + config.method + (typeof config.data === "string"?config.data:JSON.stringify(config.data))
        pending.indexOf(flagUrl) !== -1 ?
        f() && pending.splice(pending.indexOf(flagUrl), 1) :
        pending.push(flagUrl)
    }



  /* pending.indexOf(flagUrl) !== -1 ?
       f ?
           f() :
           pending.splice(pending.indexOf(flagUrl), 1)
       :
       f ?
           pending.push(flagUrl) :
           pending = []*/
}

//标识码
function guid() {
    function crack() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
    }
    return (crack() + crack() + crack() + crack())
}

//添加请求拦截器 loading
arg.interceptors.request.use(config => {
    config.headers.token = sessionStorage.getItem('token')
    if (config.method === 'post') {
        config.cancelToken = new CancelToken((c) => {
            removePending(config, c)
        })
    }
    if (config.url.indexOf("?") >= 0) {
      config.url = config.url + "&timestamp=" + guid()
    } else {
      config.url = config.url + "?timestamp=" + guid()
    }
    LoadingBar.start()
    return config
}, error => {
    setTimeout(()=>{
        pending.splice(pending.indexOf(flagUrl), 1)
    },300);
  LoadingBar.error()
    Message.error('请求失败')
    return Promise.reject(error)
})
arg.interceptors.response.use(config => {
    setTimeout(()=>{
        pending.splice(pending.indexOf(flagUrl), 1)
    },300);
  LoadingBar.finish()
    
    return config
}, error => {
    console.log(error,'error');
    setTimeout(()=>{
        pending.splice(pending.indexOf(flagUrl), 1)
    },300);
//   pending.splice(pending.indexOf(flagUrl), 1)
  LoadingBar.error()
    if (!navigator.onLine) {
        Notice.destroy()
        Notice.error({
            title: '提示',
            desc: '无网络连接'
        })
        return
    }
    // if (error.response === undefined) {
    //     Message.destroy()
    //     Message.error('网络错误')
    // }
    error.message = {
        status: error.response.status,
    }
    switch (error.response.status) {
        case 403:
            error.message.msg = '服务器拒绝请求 '
            break
        case 404:
            error.message.msg = '请求地址不存在'
            break
        case 500:
            error.message.msg = '内部服务器错误 '
            break
        case 502:
            error.message.msg = '错误的网关 '
            break
        case 503:
            error.message.msg = '服务当前不可用 '
            break
        case 504:
            error.message.msg = '服务器超时 '
            break
        case 505:
            error.message = 'http版本不支持该请求'
            break
        default:
            error.message = `连接错误${error.response.status}`
    }
    Message.destroy()
    Message.error(error.message.msg)
    return Promise.reject(error.message)
})

Vue.prototype.$post = function(url,params) {
  return new Promise((resolve,reject) => {
    arg.post(url,params).then(res=>{
      resolve(res)
    }).catch(err=>{
      reject(err)
    })
  })
}
Vue.prototype.$get = function(url,params) {
  return new Promise((resolve,reject) => {
    arg.get(url,{
      params: params
    }).then(res=>{
      resolve(res)
    }).catch(err=>{
      reject(err)
    })
  })
}
Vue.prototype.$http = arg
