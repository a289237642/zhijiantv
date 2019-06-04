export default {
  routes: {
    // 路由对应的菜单id和父节点
    classifyManagement1: { id: '1', parent: ['1'] },
    classifyManagement: { id: '2', parent: ['2'] },
    chosenManagement: { id: '3', parent: ['3'] },
    uploadVideo: { id: '4', parent: ['4'] },
  },
  login: () => import('@/views/login/login'),
  home: () => import('@/views/Home'),
  //分类管理
  classifyManagement: () => import('@/views/classifyManagement/classifyManagement'),
  //上传视频
  uploadVideo: () => import('@/views/uploadVideo/uploadVideo')
}
