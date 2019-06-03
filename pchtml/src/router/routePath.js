export default {
  routes: {
    // 路由对应的菜单id和父节点
    ActivityList: { id: '2-1', parent: ['2'] },
    tipoffList: { id: '3-1', parent: ['3'] },
    CompanyHeadline: { id: '3-2', parent: ['3'] },
    tipoffLibrary: { id: '3-3', parent: ['3'] },
    tipoffManagement: { id: '3-4', parent: ['3'] },
    bannerManagement: { id: '3-5', parent: ['3'] },
    schoolManagement: { id: '3-6', parent: ['3'] },
    iconManagement: { id: '3-7', parent: ['3'] },
    signManagement: { id: '3-8', parent: ['3'] },
    vipcnLibrary: { id: '3-9', parent: ['3'] },
    vipcnList: { id: '3-10', parent: ['3'] },
    userList: { id: '4-1', parent: ['4'] },
    lessonManagement: { id: '6-1', parent: [6] },
    lessonAudio: { id: '6-2', parent: [6] },
    headImage: { id: '6-3', parent: [6] },
    lessonLibray: { id: '6-4', parent: [6] },
    ChangePassword: { id: '5-1', parent: ['5'] },
    freeListen: { id: '7-1', parent: ['7'] },
    business: { id: '7-2', parent: ['7'] },
    typeManagement: { id: '7-3', parent: ['7'] },
    goodsList: { id: '8-1', parent: ['8'] },
    addGoods: { id: '8-2', parent: ['8'] },
    applicationLists: { id: '8-3', parent: ['8'] },
    advList: { id: '9-1', parent: ['9'] },
    channelList: { id: '11-1', parent: ['11'] },
    dataOverview: { id: '11-2', parent: ['11'] },
    spreadDetail: { id: '11-3', parent: ['11'] },
    orderList: { id: '10-1', parent: ['10'] },
    orderDetail: { id: '10-2', parent: ['10'] },
    keywordsManagement: { id: '3-11', parent: ['10'] },
    sensitivewordsManagement: { id: '3-12', parent: ['10'] }
  },
  login: () => import('@/pages/login/login'),
  home: () => import('@/pages/home'),
  //首页
  index: () => import('@/pages/index/index'),
  //活动管理
  ActivityList: () => import('@/pages/activityManagement/ActivityList'),
  //爆料管理
  tipoffList: () => import('@/pages/tipoffManagement/tipoffList'),
  CompanyHeadline: () => import('@/pages/tipoffManagement/CompanyHeadline'),
  tipoffLibrary: () => import('@/pages/tipoffManagement/tipoffLibrary'),
  tipoffManagement: () => import('@/pages/tipoffManagement/tipoffManagement'),
  iconManagement: () => import('@/pages/tipoffManagement/iconManagement'),
  signManagement: () => import('@/pages/tipoffManagement/signManagement'),
  bannerManagement: () => import('@/pages/tipoffManagement/bannerManagement'),
  schoolManagement: () => import('@/pages/tipoffManagement/schoolManagement'),
  vipcnLibrary: () => import('@/pages/tipoffManagement/vipcnLibrary'),
  vipcnList: () => import('@/pages/tipoffManagement/vipcnList'),
  //用户管理
  userList: () => import('@/pages/userManagement/userList'),
  //管理中心
  ChangePassword: () => import('@/pages/ManagementCenter/ChangePassword'),
  // 课程管理
  lessonManagement: () => import('@/pages/lessonManagement/lessonManagement'),
  //课程音频
  lessonAudio: () => import('@/pages/lessonManagement/lessonAudio'),
  //免费听
  freeListen: () => import('@/pages/perceive/freeListen'),
  //商学院
  business: () => import('@/pages/perceive/business'),
  //类型管理
  typeManagement: () => import('@/pages/perceive/typeManagement'),
  //头像库
  headImage: () => import('@/pages/lessonManagement/headImage'),
  // 课程库
  lessonLibray: () => import('@/pages/lessonManagement/lessonLibray'),
  // 商品管理
  goodsList: () => import('@/pages/goods/goodsList'),
  addGoods: () => import('@/pages/goods/addGoods'),
  applicationLists: () => import('@/pages/goods/applicationLists'),
  // 广告管理
  advList: () => import('@/pages/advmanagement/advList'),
  // 渠道管理
  channelList: () => import('@/pages/spreadManagement/channelList'),
  // 数据概览
  dataOverview: () => import('@/pages/spreadManagement/dataOverview'),
  //渠道数据详情
  spreadDetail: () => import('@/pages/spreadManagement/spreadDetail'),
  // 订单管理
  orderList: () => import('@/pages/orderManagement/orderList'),
  orderDetail: () => import('@/pages/orderManagement/orderDetail'),
  keywordsManagement: () =>
    import('@/pages/tipoffManagement/keywordsManagement'),
  sensitivewordsManagement: () =>
    import('@/pages/tipoffManagement/sensitivewordsManagement')
}
