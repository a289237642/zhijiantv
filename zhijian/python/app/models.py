# -*- coding:utf-8 -*-
from datetime import datetime

from sqlalchemy import Index

from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config.keys_config import KeysConfig


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    admin_id = db.Column(db.Integer, index=True)  # 数据的最后更新人


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "zj_user_info"

    id = db.Column(db.Integer, primary_key=True)  # 用户id
    nick_name = db.Column(db.String(32), index=True)  # 用户暱称
    nick_nameemoj = db.Column(db.String(255))  # 用户暱称
    openid = db.Column(db.String(128), unique=True, nullable=False)  # 用户open_id
    token = db.Column(db.String(255), index=True)
    phone = db.Column(db.String(11))  # 手机号
    avatar_url = db.Column(db.String(255))  # 用户头像路径
    gender = db.Column(db.String(32))  # 用户性别
    city = db.Column(db.String(32))  # 用户所属城市
    province = db.Column(db.String(32))  # 用户所属省份
    country = db.Column(db.String(32))  # 用户所属国家
    language = db.Column(db.String(32))  # 用户语言
    first_login = db.Column(db.Integer, default=1, index=True)  # 用户第一次登陆小程序的状态:0,不是第一次,1,是第一次
    login_time = db.Column(db.DateTime, default=datetime.now)  # 用户进入小程序的时间
    coins = db.Column(db.Float, default=0)  # 用户的钢镚总数
    wechat_step = db.Column(db.Integer, default=0)  # 用户当天的微信步数
    available_step = db.Column(db.Integer, default=0)  # 用户当天可用的微信步数(包含用户当天偷取的步数)
    steal_step = db.Column(db.Integer, default=0)  # 用户当天偷取的步数
    change_steal_step = db.Column(db.Integer, default=0)  # 用户当天偷取并兑换的步数
    is_sign = db.Column(db.Integer, default=0, index=True)  # 用户当天签到:0,未签到 1,已签到
    sign_time = db.Column(db.DateTime)  # 用户当天签到时间
    sign_coin = db.Column(db.Integer, default=5)  # 用户的签到奖励钢镚数

    # def to_dict(self):
    #     """将对象转换为字典数据"""
    #     user_dict = {
    #         "user_id": self.id,
    #         "name": self.name,
    #         "phone": self.phone,
    #         "avatar_url": self.avatar_url if self.avatar_url else "",
    #         "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
    #     }
    #     return user_dict


class Admin(BaseModel, db.Model):
    """管理员"""
    __tablename__ = "zj_admin_info"

    id = db.Column(db.Integer, primary_key=True)  # 用户id
    username = db.Column(db.String(128), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(128), default='e10adc3949ba59abbe56e057f20f883e')  # 用户密码
    token = db.Column(db.String(255))  # 用户标识
    is_admin = db.Column(db.Integer, default=0)  # 0:非超级管理员,1:超级管理员
    is_login = db.Column(db.Integer, default=0)  # 0:未登录,1:已登录
    status = db.Column(db.Integer, default=1)  # 用户状态,0:停用,1:启用
    auth_status = db.Column(db.Integer, default=0)  # 用户权限修改状态,0:未修改,1:已修改

    def generate_active_token(self):
        """生成激活令牌"""
        serializer = Serializer(KeysConfig.get_secret_key(), 24 * 3600)
        token = serializer.dumps({"confirm": self.id})  # 返回bytes类型
        # print 'token:', token

        return token.decode()


class Article(BaseModel, db.Model):
    """文章"""
    __tablename__ = "zj_article_info"

    id = db.Column(db.Integer, primary_key=True)  # 文章id
    title = db.Column(db.String(255), index=True)  # 文章标题
    summary = db.Column(db.String(255), default='')  # 文章简介
    author = db.Column(db.String(255), default='')  # 公众号名字,pc网站文章作者
    min_pic = db.Column(db.String(255), default='')  # 文章主图
    wechat_art_date = db.Column(db.DateTime)  # 公众号文章发布时间
    zj_art_date = db.Column(db.DateTime)  # 文章发布到小程序时间
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    is_big = db.Column(db.Integer, default=0, index=True)  # 0不突出显示　1突出显示
    web_name = db.Column(db.String(255), default='')  # pc网站名字
    link = db.Column(db.String(255), default='')  # 文章链接
    round_head_img = db.Column(db.String(255), default='')  # 公众号头像链接
    alias = db.Column(db.String(255), default='')  # 公众号的微信号
    mp3_url = db.Column(db.String(255))  # 文章语音链接
    is_read = db.Column(db.Integer)  # 0不显示语音　1显示语音
    is_original = db.Column(db.Integer)  # 0不是原创　1是原创
    read_num = db.Column(db.Integer)  # 文章阅读量(假的)


class Group(BaseModel, db.Model):
    """文章类别"""
    __tablename__ = "zj_group_info"

    id = db.Column(db.Integer, primary_key=True)  # 分类id
    name = db.Column(db.String(255))  # 分类名
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    sort_num = db.Column(db.Integer)  # 类别显示顺序号


class ArticleGroup(BaseModel, db.Model):
    """文章分类关系"""
    __tablename__ = "zj_article_group"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, index=True)
    group_id = db.Column(db.Integer, index=True)
    sort_num = db.Column(db.Integer)  # 文章上线顺序号


class Activity(BaseModel, db.Model):
    """活动"""
    __tablename__ = "zj_activity_info"

    id = db.Column(db.Integer, primary_key=True)  # 文章id
    activityid = db.Column(db.String(255), index=True)  # 活动id
    title = db.Column(db.String(255))  # 活动标题
    link = db.Column(db.String(255))  # 跳转链接
    main_img = db.Column(db.String(255))  # 活动主图
    tag = db.Column(db.String(255))  # 标签
    sort = db.Column(db.Integer)  # 排序
    status = db.Column(db.Integer)  # 状态


activity_status_index = Index('activity_status_idx', Activity.status)


class Banner(BaseModel, db.Model):
    """轮播图"""
    __tablename__ = "zj_banner_info"

    id = db.Column(db.Integer, primary_key=True)  # banner
    image = db.Column(db.String(255))  # banner 图片
    link = db.Column(db.String(255))  # 跳转id
    sort = db.Column(db.Integer)  # 排序
    status = db.Column(db.Integer, index=True)  # 状态
    article_id = db.Column(db.Integer)  # 要跳转的文章
    group_id = db.Column(db.Integer)  # 要跳转的文章所属类型


class Banner_name(BaseModel, db.Model):
    """轮播图类别"""
    __tablename__ = "zj_banner_name"

    id = db.Column(db.Integer, primary_key=True)  # banner
    name = db.Column(db.String(255))  # banner 图片
    link = db.Column(db.String(255))  # 跳转id


class Top(BaseModel, db.Model):
    """大公司头条"""
    __tablename__ = "zj_top_info"

    id = db.Column(db.Integer, primary_key=True)  # 头条id
    content = db.Column(db.String(255))  # 头条内容
    top_date = db.Column(db.DateTime)  # 头条发布时间
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    sort_num = db.Column(db.Integer)  # 头条显示顺序
    article_id = db.Column(db.Integer, index=True)  # 要跳转的文章
    group_id = db.Column(db.Integer, index=True)  # 要跳转的文章所属类型


class LessonBanner(BaseModel, db.Model):
    """banner"""
    __tablename__ = "zj_lesson_banner"

    id = db.Column(db.Integer, primary_key=True)  #
    name = db.Column(db.String(255))  #
    img_url = db.Column(db.String(255))
    jump_url = db.Column(db.String(255))
    is_big = db.Column(db.Integer, default=0, index=True)  # 0不突出显示　1突出显示


class Module(BaseModel, db.Model):
    """专栏"""
    __tablename__ = "zj_module_info"

    id = db.Column(db.Integer, primary_key=True)  # 专栏id
    name = db.Column(db.String(255))  # 专栏名字
    img_url = db.Column(db.String(255))
    jump_url = db.Column(db.String(255))


class Lesson(BaseModel, db.Model):
    """课程"""
    __tablename__ = "zj_lesson_info"

    id = db.Column(db.Integer, primary_key=True)  # 课程id
    module_id = db.Column(db.Integer, index=True)  # 课程所属专栏id
    name = db.Column(db.String(255))  # 课程名字
    author = db.Column(db.String(255))  # 主讲人
    summary = db.Column(db.String(255))  # 课程简介
    img_url = db.Column(db.String(255))  # 课程图片
    price = db.Column(db.String(255))  # 课程价格
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    jump_url = db.Column(db.String(255))


class Lesson_type(BaseModel, db.Model):
    """课程类别"""
    __tablename__ = "zj_newlesson_type"

    id = db.Column(db.Integer, primary_key=True)  # 类别id
    name = db.Column(db.String(255))  # 类别名字
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示 2免费领课
    sort = db.Column(db.Integer)  # 序号


class NewLesson(BaseModel, db.Model):
    """新课程"""
    __tablename__ = "zj_newlesson_info"

    id = db.Column(db.Integer, primary_key=True)  # 课程id
    admin_id = db.Column(db.Integer)  # 课程所属管理员id
    cost_type = db.Column(db.Integer, index=True)  # 收费类型 1 点赞  2 money 3 免费听
    title = db.Column(db.String(255), index=True)  # 课程标题
    subtitle = db.Column(db.String(255))  # 课程副标题
    author = db.Column(db.String(255))  # 主讲人
    summary = db.Column(db.String(255))  # 课程简介(1张图)
    min_pic = db.Column(db.String(255))  # 课程主图
    start_time = db.Column(db.DateTime)  # 课程开始时间
    end_time = db.Column(db.DateTime)  # 课程结束时间
    price = db.Column(db.String(255))  # 课程价格/点赞数
    present_num = db.Column(db.Integer)  # 赠送点赞数
    count = db.Column(db.Integer)  # 课程总数
    sort_num = db.Column(db.Integer)  # 课程位置序号
    is_show = db.Column(db.Integer, default=0, index=True)  # 0已下架　1已上架
    base_num = db.Column(db.Integer, default=0)  # 领取人基数
    is_open = db.Column(db.Integer, default=0, index=True)  # 免费课程的启用状态 0停用,1启用
    free_sort_num = db.Column(db.Integer)  # 免费课程的排序号
    total_audio_num = db.Column(db.Integer, default=0)  # 课程音频总数
    lesson_update_time = db.Column(db.DateTime)  # 课程音频更新时间(音频新增)


class LessonTypeShip(BaseModel, db.Model):
    """课程类别关系"""
    __tablename__ = "zj_lesson_type_ship"

    lesson_id = db.Column(db.Integer, primary_key=True)  # 课程id
    type_id = db.Column(db.Integer, primary_key=True)  # 课程类别id
    sort_num = db.Column(db.Integer)  # 课程位置序号


class LikeNum(BaseModel, db.Model):
    """点赞信息"""
    __tablename__ = "zj_likenum_info"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, index=True)  # 点赞所属订单id
    lesson_id = db.Column(db.Integer, index=True)  # 点赞所属课程id
    friend_num = db.Column(db.Integer)  # 赠送好友点赞数
    friend_user_id = db.Column(db.Integer, index=True)  # 点赞好友id


class Audio(BaseModel, db.Model):
    """课程音频信息"""
    __tablename__ = "zj_mp3_info"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, index=True)  # 音频所属课程id
    mp3_url = db.Column(db.String(255))  # 音频地址
    name = db.Column(db.String(255))  # 音频名称
    title = db.Column(db.String(255))  # 音频标题
    sort_num = db.Column(db.Integer)  # 音频位置序号
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示


class LessonOrder(BaseModel, db.Model):
    """课程订单"""
    __tablename__ = "zj_lesson_order"

    id = db.Column(db.Integer, primary_key=True)  # 课程订单id
    lesson_id = db.Column(db.Integer, index=True)  # 课程id
    user_id = db.Column(db.Integer, index=True)  # 用户id
    order_num = db.Column(db.String(255), index=True)  # 课程订单号
    wechatpay_id = db.Column(db.String(255))  # 微信支付id
    wechatpay_order_num = db.Column(db.String(255))  # 微信支付订单号
    pay_way = db.Column(db.Integer)  # 支付方式 1.点赞 2.money
    price = db.Column(db.Integer)  # 支付金额/点赞数
    help_num = db.Column(db.Integer, default=0)  # 好友点赞数
    is_help = db.Column(db.Integer, default=0, index=True)  # 是否有好友助力 0.无 1.有
    is_pay = db.Column(db.Integer, default=0)  # 是否支付 0.未支付 1.已支付
    order_status = db.Column(db.Integer, default=1, index=True)  # 订单状态 1.进行中 2.助力成功 3.助力失败
    pay_time = db.Column(db.DateTime)  # 支付时间
    is_get_present_num = db.Column(db.Integer, default=0)  # 用户是否已经得到过助力好友赠送的点赞数:0,不是,1,是
    is_send = db.Column(db.Integer, default=0, index=True)  # 0 未发送, 1 已发送 (模板消息)
    is_new = db.Column(db.Integer, default=0)  # 订单课程更新状态: 0,无更新 1,有更新
    lesson_update_time = db.Column(db.DateTime)  # 订单课程更新时间


class Icon(BaseModel, db.Model):
    """icon管理"""
    __tablename__ = "zj_icon_info"

    id = db.Column(db.Integer, primary_key=True)  # icon id
    name = db.Column(db.String(255))  # icon名称
    pic = db.Column(db.String(255))  # icon图片
    jump_url = db.Column(db.String(255))  # icon跳转小程序路径


class Poster(BaseModel, db.Model):
    """签到海报管理"""
    __tablename__ = "zj_poster_info"

    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(255))  # 海报图片
    jump_url = db.Column(db.String(255))  # 海报跳转小程序路径
    is_show = db.Column(db.Integer, default=0)  # 0:关闭,1:开启
    start_time = db.Column(db.DateTime)  # 海报开始的时间
    end_time = db.Column(db.DateTime)  # 海报结束的时间


class UserImage(BaseModel, db.Model):
    """头像库"""
    __tablename__ = "zj_user_image"

    id = db.Column(db.Integer, primary_key=True)  # 头像 id
    pic = db.Column(db.String(255))  # 头像图片链接


class ImageLesson(BaseModel, db.Model):
    """头像课程关系"""
    __tablename__ = "zj_user_image_info"

    image_id = db.Column(db.Integer, primary_key=True)  # 头像ID
    lesson_id = db.Column(db.Integer, primary_key=True)  # 课程ID


class BusinessCollege(BaseModel, db.Model):
    """商学院"""
    __tablename__ = "zj_business_college_info"

    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(255))  # 图片
    jump_url = db.Column(db.String(255))  # 跳转小程序路径
    is_show = db.Column(db.Integer, default=0)  # 0:关闭,1:开启
    appid = db.Column(db.String(255))  # appid


class UserFormID(BaseModel, db.Model):
    """from_ID收集"""
    __tablename__ = "zj_formid_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)  # 用户id
    openid = db.Column(db.String(255))  # 用户openID
    form_id = db.Column(db.String(255))  # 用户推送码


class UserBTN(BaseModel, db.Model):
    """uer_btn收集"""
    __tablename__ = "zj_user_btn"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)  # 用户id
    btn_num = db.Column(db.Integer, index=True)  # but代号 1,文章 2,课程 3,头条 4,banner 5,用户点击btn通知, 6,步数兑换等btn通知
    is_send = db.Column(db.Integer, default=0)  # 0,未发送 1,已发送
    is_new = db.Column(db.Integer, default=0)  # 文章更新状态: 0,无更新 1,有更新


class UpdateTime(BaseModel, db.Model):
    """更新时间"""
    __tablename__ = "zj_update_time"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, index=True)  # 1,文章 2,已购课程 3,线上所有课程 4,头条 5,banner图
    # is_send = db.Column(db.Integer, default=0)  # 0,未发送 1,已发送


class BornQrNum(BaseModel, db.Model):
    """课程二维码生成总数"""
    __tablename__ = "zj_born_qrnum"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer)
    # user_id = db.Column(db.Integer)
    num = db.Column(db.Integer)  # 生成总数
    btn = db.Column(db.Integer)  # 1,邀友听课 2,邀友鼓励


class ScanQrNum(BaseModel, db.Model):
    """用户分享二维码识别总数"""
    __tablename__ = "zj_scan_qrnum"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, index=True)
    # user_id = db.Column(db.Integer)  # 二维码所属用户
    num = db.Column(db.Integer)  # 识别总数
    btn = db.Column(db.Integer)  # 1,邀友听课 2,邀友鼓励


class DailyBornQrNum(BaseModel, db.Model):
    """每日二维码生成数量"""
    __tablename__ = "zj_daily_bron_qrnum"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, index=True)
    # user_id = db.Column(db.Integer)
    record_time = db.Column(db.Date, default=datetime.now)
    daily_num = db.Column(db.Integer)  # 每日生成数量
    btn = db.Column(db.Integer)  # 1,邀友听课 2,邀友鼓励


class DailyScanQrNum(BaseModel, db.Model):
    """每日二维码识别数量"""
    __tablename__ = "zj_daily_scan_qrnum"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, index=True)
    # user_id = db.Column(db.Integer)  # 二维码所属用户
    record_time = db.Column(db.Date, default=datetime.now)
    daily_num = db.Column(db.Integer)  # 每日识别数量
    btn = db.Column(db.Integer)  # 1,邀友听课 2,邀友鼓励


class ZhiHuData(BaseModel, db.Model):
    """抓取知乎问答数据"""
    __tablename__ = "zj_zhihu_info"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255))  # 原文链接
    title = db.Column(db.String(255))  # 问题标题
    content = db.Column(db.String(255))  # 问题内容
    theme = db.Column(db.String(255))  # 问题话题
    publish_time = db.Column(db.DateTime)  # 问题发布时间
    updated_time = db.Column(db.DateTime)  # 问题更新时间
    author = db.Column(db.String(128))  # 问题作者
    img = db.Column(db.String(255))  # 问题作者头像
    view_num = db.Column(db.Integer)  # 问题浏览量
    attention_num = db.Column(db.Integer)  # 问题关注量
    keywords = db.Column(db.String(128))  # 问题关键字
    # answer = db.Column(db.String(255))  # 问题答案


class WeChatName(BaseModel, db.Model):
    # 公众号库
    __tablename__ = "zj_webname_info"
    id = db.Column(db.Integer, primary_key=True)
    wechat_name = db.Column(db.String(128))  # 公众号名称
    alias = db.Column(db.String(255))  # 公众号的微信号
    is_show = db.Column(db.Integer, default=0, index=True)  # 0,没有对应公众号, 1,已有对应公众号


class WeChatNameGroup(BaseModel, db.Model):
    """公众号与自动上线的类别"""
    __tablename__ = "zj_webname_group"

    wechat_id = db.Column(db.Integer, primary_key=True)  # 公众号ID
    group_id = db.Column(db.Integer, primary_key=True)  # 公众号下文章对应的上线类别ID


class Sales(BaseModel, db.Model):
    # 推广人员
    __tablename__ = "zj_sales_info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class SalesNum(BaseModel, db.Model):
    # 推广总数
    __tablename__ = "zj_sales_num"
    sales_id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, default=1)


class DailySalesQrNum(BaseModel, db.Model):
    """每日二维码识别数量"""
    __tablename__ = "zj_daily_sales_num"

    id = db.Column(db.Integer, primary_key=True)
    sales_id = db.Column(db.Integer, index=True)
    lesson_id = db.Column(db.Integer, index=True)
    record_time = db.Column(db.Date, default=datetime.now)
    daily_num = db.Column(db.Integer)  # 每日识别数量


class NewsData(BaseModel, db.Model):
    # 资讯途听快讯
    __tablename__ = "zj_news_info"
    id = db.Column(db.Integer, primary_key=True)
    web_name = db.Column(db.String(128))  # 来源名称
    base_url = db.Column(db.String(128))  # 来源链接
    audio_url = db.Column(db.String(255))  # 音频链接
    publish_time = db.Column(db.DateTime)  # 原发布时间
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    listen_num = db.Column(db.Integer)  # 已听数量
    zj_art_date = db.Column(db.DateTime)  # 上线时间
    title = db.Column(db.String(255))  # 快讯标题
    has_content = db.Column(db.Integer, index=True)  # 1,有详情 0,无详情
    is_read = db.Column(db.Integer)  # 0不显示语音　1显示语音 2没有音频
    # content = db.Column(db.String(255))


class NewsGroup(BaseModel, db.Model):
    # 资讯途听快讯分类
    __tablename__ = "zj_newsgroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))  # 名称
    sort_num = db.Column(db.Integer)
    is_show = db.Column(db.Integer, default=0, index=True)  # 0不显示　1显示
    listen_num = db.Column(db.Integer)  # 已听数量


class NewsGroupInfo(BaseModel, db.Model):
    # 资讯途听快讯分类关系
    __tablename__ = "zj_newsgroup_info"
    news_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)
    sort_num = db.Column(db.Integer)
    publish_time = db.Column(db.DateTime)  # 原发布时间


class UserSteps(BaseModel, db.Model):
    # 用户兑换步数记录
    __tablename__ = "zj_user_steps_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    change_step_date = db.Column(db.DateTime, index=True)  # 用户兑换时的时间
    change_step = db.Column(db.Integer)  # 用户兑换的步数
    # steal_step = db.Column(db.Integer)  # 用户偷取的步数
    get_coins = db.Column(db.Float)  # 用户兑换获得的钢镚
    random_coin = db.Column(db.Float)  # 用户兑换后转发获得的钢镚
    openGId = db.Column(db.String(255), index=True)  # 用户分享到的微信群的唯一标识


class UserFriends(BaseModel, db.Model):
    # 用户好友记录
    __tablename__ = "zj_user_friends_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    friend_id = db.Column(db.Integer, index=True)
    steal_num = db.Column(db.Integer, default=2)  # 可偷取好友次数, 每个好友默认最多两次
    steal_date = db.Column(db.DateTime, index=True)  # 偷取时间


class UserReadArticle(BaseModel, db.Model):
    # 用户阅读文章奖励记录
    __tablename__ = "zj_user_read_article"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    article_id = db.Column(db.Integer, index=True)
    random_coins = db.Column(db.Float)  # 用户阅读获得随机奖励值
    # coin = db.Column(db.Integer, default=1)


class UserShareArticle(BaseModel, db.Model):
    # 用户分享文章奖励记录
    __tablename__ = "zj_user_share_article"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    article_id = db.Column(db.Integer, index=True)
    # friend_id = db.Column(db.Integer)
    openGId = db.Column(db.String(255))  # 用户分享到的微信群的唯一标识
    random_coins = db.Column(db.Float)  # 用户分享获得随机奖励值


class UserSign(BaseModel, db.Model):
    # 用户每日签到奖励记录
    __tablename__ = "zj_user_sign_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    sign_coin = db.Column(db.Integer)  # 签到奖励
    openGId = db.Column(db.String(255), index=True)  # 用户分享到的微信群的唯一标识
    random_coin = db.Column(db.Float)  # 签到后转发的随机奖励


class Goods(BaseModel, db.Model):
    # 商品
    __tablename__ = "zj_goods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # 商品名字
    # img_url = db.Column(db.String(255))
    detail = db.Column(db.String(1024))  # 商品详情
    ku_num = db.Column(db.Integer)  # 库存
    available_num = db.Column(db.Integer)  # 可兑换数量
    price = db.Column(db.Integer)  # 价格
    postage = db.Column(db.Float)  # 邮费
    is_show = db.Column(db.Integer, default=1, index=True)  # 1,上架状态 -1,下架状态


class GoodsImage(BaseModel, db.Model):
    # 商品的轮播图
    __tablename__ = "zj_goods_img"

    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, index=True)
    img_url = db.Column(db.String(255))
    is_min = db.Column(db.Integer, default=0, index=True)  # 商品头图: 0,不是 1,是


class UserAddress(BaseModel, db.Model):
    # 用户收货地址
    __tablename__ = "zj_user_address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(11))
    provence = db.Column(db.String(128))
    city = db.Column(db.String(128))
    area = db.Column(db.String(128))
    detail = db.Column(db.String(255))
    post_num = db.Column(db.Integer)


class GoodsOrder(BaseModel, db.Model):
    # 用户商品订单
    __tablename__ = "zj_goods_order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    goods_id = db.Column(db.Integer, index=True)
    address_id = db.Column(db.Integer, index=True)  # 收货地址
    order_num = db.Column(db.String(255), index=True)  # 订单号
    refund_order_num = db.Column(db.String(255))  # 订单号
    refund_id = db.Column(db.String(255), index=True)  # 微信退款成功返回的订单号
    transaction_id = db.Column(db.String(255), index=True)  # 微信支付成功返回的订单号
    wx_code = db.Column(db.String(255))  # 微信支付状态
    pay_time = db.Column(db.String(64))  # 微信返回的支付完成时间
    send_time = db.Column(db.DateTime)  # 发货时间
    receive_time = db.Column(db.DateTime)  # 签收时间
    close_time = db.Column(db.DateTime)  # 超时关闭时间
    refund_time = db.Column(db.DateTime)  # 退款时间
    refund_person = db.Column(db.DateTime)  # 退款人
    postage = db.Column(db.Integer)  # 支付金额(邮费)
    price = db.Column(db.Integer)  # 支付钢镚数
    order_status = db.Column(db.Integer, default=1, index=True)  # 1:待付款(邮费) 2:待发货 3:待收货 4:已完成 5:超时自动关闭 -1:申请退款, -2:退款成功


class ExpressInfo(BaseModel, db.Model):
    # 商品订单物流信息
    __tablename__ = "zj_express_info"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, index=True)  # 订单ID
    express_num = db.Column(db.String(255))  # 快递单号
    company = db.Column(db.String(128))  # 快递公司
    remark = db.Column(db.String(255))  # 备注


class ChangeAmount(BaseModel, db.Model):
    # 换量的小程序信息
    __tablename__ = "zj_change_amount"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # 换量的小程序名称
    app_id = db.Column(db.String(255))  # 换量的小程序app_id
    img_url = db.Column(db.String(255))  # 换量的小程序海报图片
    sort_num = db.Column(db.Integer, default=1)  # 排序位置
    is_show = db.Column(db.Integer, default=1, index=True)  # 1,显示 0,隐藏
    coin = db.Column(db.Integer)  # 奖励钢镚值
    words = db.Column(db.String(255))  # 换量的小程序自定义文字
    path = db.Column(db.String(255))  # 换量的小程序自定义跳转路径


class ChangeAmountUser(BaseModel, db.Model):
    # 用户获取换量的小程序奖励记录表
    __tablename__ = "zj_change_amount_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    mini_program_id = db.Column(db.Integer, index=True)
    coin = db.Column(db.Integer)  # 获得的奖励值
    start_time = db.Column(db.DateTime)  # 试玩开始时间
    end_time = db.Column(db.DateTime)  # 试玩结束时间


class AfterPlayShare(BaseModel, db.Model):
    # 用户获取换量的小程序奖励后分享奖励记录表
    __tablename__ = "zj_change_amount_share_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    mini_program_id = db.Column(db.Integer, index=True)
    openGId = db.Column(db.String(255), index=True)  # 用户分享到的微信群的唯一标识
    random_coins = db.Column(db.Float)  # 试完后转发获得的奖励


class BlackAccount(BaseModel, db.Model):
    """小程序接口访问黑名单"""
    __tablename__ = "zj_black_account"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255))  # 非法访问的ip
    openid = db.Column(db.String(255), index=True)  # 非法访问的openID
    num = db.Column(db.Integer, default=1)  # 1分钟内的访问次数


class ArticleKeyWords(BaseModel, db.Model):
    """文章分类标签关键词"""
    __tablename__ = "zj_article_keywords"

    id = db.Column(db.Integer, primary_key=True)
    article_group_id = db.Column(db.Integer, index=True)
    first_keywords = db.Column(db.String(255))
    second_keywords = db.Column(db.String(255))


class ArticleSensitiveWords(BaseModel, db.Model):
    """文章过滤敏感词"""
    __tablename__ = "zj_sensitive_words"

    id = db.Column(db.Integer, primary_key=True)
    sensitive_words = db.Column(db.String(255))


class SpreadName(BaseModel, db.Model):
    """推广渠道"""
    __tablename__ = "zj_spread_name"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    spread_type_id = db.Column(db.Integer, index=True)
    spread_url = db.Column(db.String(255))
    is_del = db.Column(db.Integer, default=1, index=True)  # 逻辑删除, 1,存在, -1,已删除


class SpreadRecord(BaseModel, db.Model):
    """推广记录"""
    __tablename__ = "zj_spread_record"

    id = db.Column(db.Integer, primary_key=True)
    spread_id = db.Column(db.Integer, index=True)
    openid = db.Column(db.String(128), unique=True)
    spread_type_id = db.Column(db.Integer, index=True)
    is_auth = db.Column(db.Integer, default=1, index=True)  # 是否授权, 1,授权, -1,未授权
    is_del = db.Column(db.Integer, default=1, index=True)  # 逻辑删除, 1,存在, -1,已删除


class SpreadType(BaseModel, db.Model):
    """推广方式"""
    __tablename__ = "zj_spread_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class TestTest(BaseModel, db.Model):
    """测试数据"""
    __tablename__ = "zj_test_test"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class LookVideoRecord(BaseModel, db.Model):
    # 用户看视奖励（金币）
    __tablename__ = "zj_look_video_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    coin = db.Column(db.Integer)  # 获得的奖励值
    start_time = db.Column(db.DateTime)  # 试玩开始时间
    end_time = db.Column(db.DateTime)  # 试玩结束时间


class UserAtmRecord(BaseModel, db.Model):
    # 用户提现记录
    __tablename__ = "zj_user_atm_record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    openid = db.Column(db.String(255))  # 用户openID
    coin = db.Column(db.Float, default=0)  # 花销金币
    atm_num = db.Column(db.Integer, index=True)  # 提取金额  以分为单位存储计算
    nonce_str = db.Column(db.String(100))  # 随机字符串
    trade_no = db.Column(db.String(100))  # 商户订单号
    ip = db.Column(db.String(50))  # 客户端ip


class HeavenForUserOpen(BaseModel, db.Model):
    # 天降红包 新增用户关系
    __tablename__ = "zj_heaven_for_user"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)  # 发起邀请用户id
    openid = db.Column(db.String(128))  # 用户open_id
    new_openid = db.Column(db.String(128))  # 用户open_id
    new_user_id = db.Column(db.Integer, index=True)  # 新用户id
    status = db.Column(db.Integer, default=0)  # 新用户 0 = 未兑换钢镚  1已经兑换


class HeavenRedRecord(BaseModel, db.Model):
    # 天降红包 兑换钢镚记录
    # 邀请1个新授权用户奖0.3元  = 300 coins
    # 邀请2个新授权用户奖0.6元
    # 邀请3个新授权用户奖1元
    __tablename__ = "zj_heaven_red_record"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)  # 用户id
    user_s_id = db.Column(db.String(50))
    coins = db.Column(db.Float, default=0)  # 兑换钢镚记录


class RedOpneDay(BaseModel, db.Model):
    # 每日开红包
    __tablename__ = "zj_red_open_day"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)  # 用户id
    coins = db.Column(db.Float, default=0)  # 开出钢镚数量


class ChangeClickStatistics(BaseModel, db.Model):
    # 换量点击次数统计
    __tablename__ = "zj_change_click_count"
    id = db.Column(db.Integer, primary_key=True)
    amount_id = db.Column(db.Integer)  # 换量渠道id
    btn_nums = db.Column(db.Integer)  # 点击次数统计
    btn_successful_nums = db.Column(db.Integer)  # 点击成功次数统计

