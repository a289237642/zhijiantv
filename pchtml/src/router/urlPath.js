export default {
  LOGIN: '/api/v1_0/login', //登陆
  LOGINOUT: '/api/v1_0/logout', //登出
  CHANGEPWD: '/api/v1_0/changwpwd', //修改密码
  GETPCACTIVITY: '/api/v1_0/getpcactivity', //获取活动列表
  CREATEACTIVITY: '/api/v1_0/createactivity', //创建活动
  CHANGEACTIVITY: '/api/v1_0/changeactivity', //编辑活动
  CHANGESTATUS: '/api/v1_0/changestatus', //修改活动状态
  UPLOADIMAGE: '/api/v1_0/uploadimage', //base64上传图片
  GETPXBANNER: '/api/v1_0/getpcbanner', //banner列表
  CHANGEBANNERTATUS: '/api/v1_0/changebannertatus', //修改banner状态
  DELETEBANNER: '/api/v1_0/deletebanner', //删除banner
  CREATEBANNER: '/api/v1_0/createbanner', //创建banner
  CHANGEBANNER: '/api/v1_0/changebanner', //修改banner

  GETUSERLIST: '/api/v1_0/getuserlist', //获取用户列表
  PCTOPS: 'api/v1_0/pc_tops', //获取头条列表
  UPLOADTOP: '/api/v1_0/upload_top', //隐藏或发布头条
  DELTOP: '/api/v1_0/del_top', //删除头条
  ADDTOP: '/api/v1_0/add_top', //添加、修改头条

  ARTICLEGROUP: '/api/v1_0/pc_article_group', //获取爆料分类列表
  ARTICLES: '/api/v1_0/articles', //获取爆料全部列表
  ARTICALSEARCH: '/api/v1_0/article_search', //爆料库搜索
  DOWNLINE: '/api/v1_0/down_line', //下线

  PCGROUPS: '/api/v1_0/pc_groups', //爆料类型列表
  ARTICLESSearch: '/api/v1_0/article_search', //搜索爆料库
  DELARTICLE: '/api/v1_0/del_article', //删除爆料库
  ONLINE: '/api/v1_0/upload_article', //设置上线
  MINPIC: '/api/v1_0/min_pic', //修改文章头图
  UODATEGROUP: 'api/v1_0/update_group', //修改爆料类型
  DELGROUP: 'api/v1_0/del_group', //删除爆料类型
  STARTGROUP: 'api/v1_0/start_group', //爆料库类型启用禁用
  GROUPSEARCH: 'api/v1_0/group_search', //爆料类型搜索
  SHOWBIG: 'api/v1_0/show_big', //爆料列表突出显示
  CURRENTGROUP: 'api/v1_0/current_group', //获取文章所属分类
  SETARTICLE: 'api/v1_0/set_article', //爆料列表设置
  GROUPS: 'api/v1_0/groups', //跳转文章类型
  WECHATURL: 'api/v1_0/wechat_url', //单篇文章获取
  ARTICLESOURCE: 'api/v1_0/article_source', //获取文章来源
  ARTICLEDETAILS: 'api/v1_0/pc_article_details', //获取文章详情
  GETAUDIO: 'api/v1_0/get_audio', //文章转语音
  //文章标签管理
  KEYWORDLIST: '/api/v1_0/article_keyword_list', //获取文章分类关键词列表
  KEYWORDADD: '/api/v1_0/article_keyword_add', // 文章关键词新增
  KEYWORDUPLOAD: '/api/v1_0/article_keyword_update', // 文章关键词修改
  DELKEYWORD: '/api/v1_0/del_article_keyword', // 文章分类关键词删除
  //文章敏感词管理
  SENSITIVEWORDSLS: '/api/v1_0/sensitive_words_ls', // 敏感词展示
  SENSITIVEWORDSUPDATE: '/api/v1_0/sensitive_words_update', // 敏感词增加修改
  DELSENSITIVEWORDS: '/api/v1_0/del_sensitive_words', //敏感词删除

  GET_PCLESSONS: '/api/v1_0/get_pclessons',
  EDIT_LESSONS: '/api/v1_0/edit_lessons',
  ONLINESearch: '/api/v1_0/online_article_search', //搜索爆料列表

  PCICONLIST: '/api/v1_0/pc_icon_list', //获取icon列表
  UPDATEICON: '/api/v1_0/update_icon', //修改或增加icon
  PCPOSTERLIST: '/api/v1_0/pc_poster_list', //pc签到海报获取
  UPDATEPOSTER: '/api/v1_0/update_poster', //PC修改或增加海报
  PCLESSONS: '/api/v1_0/pc_lessons', //PC课程列表
  LESSONMOVE: '/api/v1_0/lesson_move', //课程移动
  UPLOADLESSONS: '/api/v1_0/upload_lessons', //上架课程
  DOWNLESSON: '/api/v1_0/down_lessons', //下架课程
  DELETELESSON: '/api/v1_0/delete_lesson', //PC删除课程
  ADDLESSON: '/api/v1_0/add_lesson', //PC新增课程
  EDITLESSON: '/api/v1_0/edit_lesson', //PC修改课程
  PCLESSONDETAIL: '/api/v1_0/pc_lesson_detail', //PC课程详情
  LESSONAUDIOLIST: '/api/v1_0/lesson_audio_list', //PC课程音频列表
  AUDIOMOVE: '/api/v1_0/audio_move', //移动音频
  DELLESSONAUDIN: '/api/v1_0/del_lesson_audio', //删除课程音频
  ADDLESSONAUDIO: '/api/v1_0/add_lesson_audio', //新增课程音频
  LESSONPERSONS: '/api/v1_0/lesson_persons', //参与用户
  GETLESSONDOWN: '/api/v1_0/lesson_down', //获取下架课程
  PCGETLESSONTYPE: '/api/v1_0/pc_get_lesson_type', //获取课程类别列表
  DEL_FREE_LESSON: '/api/v1_0/del_free_lesson', //获取课程类别列表

  PC_FREE_LESSONS: '/api/v1_0/pc_free_lessons', //今日免费全部听列表
  PC_LESSONS: '/api/v1_0/pc_lessons', //今日免费全部听列表
  ADD_FREE_LESSON: '/api/v1_0/add_free_lesson', //今日免费全部列表
  UPDATE_FREE_LESSON: '/api/v1_0/update_free_lesson', //编辑免费课程/自定义排序
  OPEN_FREE_LESSON: '/api/v1_0/open_free_lesson', //今日免费启用或停用
  GET_PC_BUSSINESS: '/api/v1_0/get_pc_bussiness', //智见商学院列表
  CREATE_BUSSINESS: '/api/v1_0/create_bussiness', //新增修改智见商学院
  GET_LESSON_TYPE: '/api/v1_0/pc_get_lesson_type', //获取类别列表
  EDIT_LESSON_TYPE: '/api/v1_0/edit_lesson_type', //编辑课程类别
  ADD_LESSON_TYPE: '/api/v1_0/add_lesson_type', //新增课程类别
  DELETE_LESSON_TYPE: '/api/v1_0/delete_lesson_type', //新增课程类别
  STATUS_LESSON_TYPE: '/api/v1_0/status_lesson_type', //修改课程类别状态
  LESSON_SEARCH: '/api/v1_0/lesson_search', //搜索
  UPUPUP: '/api/v1_0/upupup', //头像上传
  IMAGE_STORE: '/api/v1_0/image_store', //头像列表
  DEL_IMAGE: '/api/v1_0/del_image', //头像删除
  PCLESSSONLIST: '/api/v1_0/pc_lesson_list', //课程分类列表

  WECHATNAMELIST: '/api/v1_0/wechat_name_list', //公众号库获取
  ADDWECHATNAME: '/api/v1_0/add_wechat_name', //公众号添加
  SETWECHATGROUP: '/api/v1_0/set_wechat_group', //公众号设置
  RESETWECHATGROUP: '/api/v1_0/reset_wechat_group', //公众号重设
  WECHATNAMEGROUP: '/api/v1_0/wechat_name_group', //公众号分类列表
  DELWECHATNAME: '/api/v1_0/del_wechat_name', //公众号删除

  USERSEARCH: '/api/v1_0/user_search', //用户列表搜索
  PCARTICLETITLE: '/api/v1_0/pc_article_title', //获取跳转文章列表

  // 商品管理===========================================
  GOODSLIST: '/api/v1_0/pc_goods_list', // 商品列表
  GOODSDOWN: '/api/v1_0/goods_down', // 上架/下架
  GOODSDEL: '/api/v1_0/goods_del', // 删除商品
  PCGOODSDETAIL: '/api/v1_0/pc_goods_detail', // 商品详情
  UPIMAGE: '/api/v1_0/up_image', // 图片上传
  GOODSUPDATE: '/api/v1_0/goods_update', // 新增或修改商品
  GOODSQUERY: '/api/v1_0/pc_goods_query', // 商品列表搜索
  GOODSUSERINFO: '/api/v1_0/goods_user_info', // 当前商品已下单的用户信息
  //换量================================================
  MINIPROGRAMLS: '/api/v1_0/mini_program_ls', // 换量小程序列表
  MINICHANGESTATUS: '/api/v1_0/mini_program_change_status', // 改变换量小程序的状态
  DELMINIPROGRAM: '/api/v1_0/del_mini_program', // 换量小程序删除
  UPDATEMINIPROGRAM: '/api/v1_0/update_mini_program', // 新增或修改换量小程序信息
  PCGOODSORDERLS: '/api/v1_0/pc_goods_order_ls', // 订单分类列表
  BULKSENDGOODS: '/api/v1_0/bulk_send_goods', // 发货
  PCGOODSORDERDETAIL: '/api/v1_0/pc_goods_order_detail', // 订单详情
  PCGOODSORDERCLOSE: '/api/v1_0/pc_goods_order_close', // 订单关闭
  PCEXPRESSINFO: '/api/v1_0/pc_express_info', //订单的物流信息
  //推广=================================================
  SPREADNAMELS: '/api/v1_0/spread_name_ls', //渠道列表
  SPREADTYPE: '/api/v1_0/spread_type', //渠道推广方式
  SPREADNAMEUPDATE: '/api/v1_0/spread_name_update', // 渠道增加/修改
  GENERATESPERATEURL: '/api/v1_0/generate_spread_url', // 生成渠道链接
  SPREADNAMEDEL: '/api/v1_0/spread_name_del', // 渠道删除
  SPREADNAMESEARCH: '/api/v1_0/spread_name_search', //渠道名称搜索
  SPREADDATALS: '/api/v1_0/spread_data_ls', // 渠道数据概览（默认当日数据）
  SPREADDATADETAIL: '/api/v1_0/spread_data_detail', //渠道数据详情
  SPREADDATAQUERYBYDATE: '/api/v1_0/spread_data_query_by_date', // 渠道数据按日期查询
  SPREADDATASEARCH: '/api/v1_0/spread_data_search' //渠道数据搜索
}
