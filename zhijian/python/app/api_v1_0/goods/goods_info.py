# -*- coding:utf-8 -*-
# author: will

# 新增或修改商品
import base64

from flask import request, jsonify, g

from app import db
from app.models import Goods, GoodsOrder, User, GoodsImage
from utils.log_service import Logging
from utils.user_service.login import auth_required, login_required, admin_required
from . import api_goods


# PC新增或修改商品
@api_goods.route('/goods_update', methods=['POST'])
@login_required
@admin_required
def goods_update():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')
        name = res.get('name')
        price = res.get('price')
        ku_num = res.get('ku_num')
        detail = res.get('detail')
        # {'image_data':[{'img_url':'http:xxx','is_min':1},{'img_url':'http:xxx','is_min':0}]}
        image_data = res.get('image_data')
        # img_url = res.get('img_url')
        postage = res.get('postage')
        admin_id = g.user_id

        Logging.logger.info('request_args:{0}'.format(res))
        if not all([name, price, ku_num, image_data, postage]):
            return jsonify(errno=-1, errmsg='参数不完整')

        try:
            price = int(price)
            ku_num = int(ku_num)
            postage = int(postage)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        if goods_id:
            # 修改
            try:
                goods_id = int(goods_id)
            except Exception as e:
                Logging.logger.error('errmsg:{0}'.format(e))
                return jsonify(errno=-1, errmsg='参数错误')

            goods_obj = Goods.query.get(goods_id)
            if not goods_obj:
                return jsonify(errno=-1, errmsg='当前商品不存在')

            goods_obj.name = name
            goods_obj.price = price
            now_available_num = ku_num - (goods_obj.ku_num - goods_obj.available_num)

            if now_available_num < 0:
                return jsonify(errno=-1, errmsg='商品库存数量不能小于原已兑换数量')

            goods_obj.available_num = now_available_num
            goods_obj.ku_num = ku_num
            goods_obj.detail = detail
            goods_obj.postage = postage
            goods_obj.admin_id = admin_id
            # goods_obj.img_url = img_url

            if image_data:
                # 删除原有的商品轮播图片
                goods_img = GoodsImage.query.filter(GoodsImage.goods_id == goods_id).all()
                for img in goods_img:
                    db.session.delete(img)

                # 添加新的图片
                for image in image_data:
                    image_obj = GoodsImage()
                    image_obj.goods_id = goods_id
                    image_obj.img_url = image.get('img_url')
                    image_obj.is_min = image.get('is_min')
                    db.session.add(image_obj)

            db.session.add(goods_obj)

        else:
            # 新增
            goods = Goods.query.filter(Goods.name == name).first()
            if goods:
                return jsonify(errno=-1, errmsg='该商品名称已经存在')

            goods_obj = Goods()
            goods_obj.name = name
            goods_obj.price = price
            goods_obj.ku_num = ku_num
            goods_obj.available_num = ku_num
            goods_obj.detail = detail
            goods_obj.postage = postage
            goods_obj.admin_id = admin_id
            # goods_obj.img_url = img_url

            db.session.add(goods_obj)
            db.session.commit()

            for image in image_data:
                image_obj = GoodsImage()
                image_obj.goods_id = goods_obj.id
                image_obj.img_url = image.get('img_url')
                image_obj.is_min = image.get('is_min')
                db.session.add(image_obj)

        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='更新商品失败')


# PC商品列表
@api_goods.route('/pc_goods_list', methods=['POST'])
@login_required
@admin_required
def pc_goods_list():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        is_show = res.get('is_show')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if is_show:
            # -1,已下架,1,进行中
            if isinstance(is_show, int):
                if is_show not in [-1, 1]:
                    return jsonify(errno=-1, errmsg='参数错误')
            else:
                return jsonify(errno=-1, errmsg='参数错误')

            results = Goods.query.filter(Goods.is_show == is_show).order_by(Goods.create_time.desc()).paginate(page,
                                                                                                               pagesize,
                                                                                                               False)
        else:
            results = Goods.query.order_by(Goods.create_time.desc()).paginate(page, pagesize, False)
        count = results.total

        goods_ls = list()
        for goods_obj in results.items:
            goods_dict = dict()
            goods_dict['goods_id'] = goods_obj.id
            goods_dict['goods_name'] = goods_obj.name
            goods_dict['price'] = goods_obj.price
            goods_dict['ku_num'] = goods_obj.ku_num  # 库存
            goods_dict['available_num'] = goods_obj.available_num  # 剩余可用库存
            goods_dict['change_num'] = int(goods_obj.ku_num) - int(goods_obj.available_num)  # 已兑换数量
            goods_dict['create_time'] = str(goods_obj.create_time)
            goods_dict['is_show'] = goods_obj.is_show
            goods_dict['postage'] = goods_obj.postage
            # goods_dict['img_url'] = goods_obj.img_url

            # 当前商品的主图
            image_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_obj.id, GoodsImage.is_min == 1).first()
            if image_obj:
                goods_dict['min_pic'] = image_obj.img_url

            goods_ls.append(goods_dict)
        return jsonify(errno=0, errmsg="OK", count=count, data=goods_ls)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品列表失败')


# PC商品列表搜索
@api_goods.route('/pc_goods_query', methods=['POST'])
@login_required
@admin_required
def pc_goods_query():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)
        goods_name = res.get('goods_name')
        is_show = res.get('is_show')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        if is_show:
            # -1,已下架,1,进行中
            if isinstance(is_show, int):
                if is_show not in [-1, 1]:
                    return jsonify(errno=-1, errmsg='参数错误')
            else:
                return jsonify(errno=-1, errmsg='参数错误')

            if goods_name:
                results = Goods.query.filter(Goods.is_show == is_show,
                                             Goods.name.like("%" + goods_name + "%")).order_by(
                    Goods.create_time.desc()).paginate(page, pagesize, False)
            else:
                results = Goods.query.filter(Goods.is_show == is_show).order_by(
                    Goods.create_time.desc()).paginate(page, pagesize, False)
        else:
            if goods_name:
                results = Goods.query.filter(Goods.name.like("%" + goods_name + "%")).order_by(
                    Goods.create_time.desc()).paginate(page, pagesize, False)
            else:
                results = Goods.query.order_by(Goods.create_time.desc()).paginate(page, pagesize, False)
        count = results.total

        goods_ls = list()
        for goods_obj in results.items:
            goods_dict = dict()
            goods_dict['goods_id'] = goods_obj.id
            goods_dict['goods_name'] = goods_obj.name
            goods_dict['price'] = goods_obj.price
            goods_dict['ku_num'] = goods_obj.ku_num  # 库存
            goods_dict['available_num'] = goods_obj.available_num  # 剩余可用库存
            goods_dict['change_num'] = int(goods_obj.ku_num) - int(goods_obj.available_num)  # 已兑换数量
            goods_dict['create_time'] = str(goods_obj.create_time)
            goods_dict['is_show'] = goods_obj.is_show
            goods_dict['postage'] = goods_obj.postage
            # goods_dict['img_url'] = goods_obj.img_url

            # 当前商品的主图
            image_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_obj.id, GoodsImage.is_min == 1).first()
            if image_obj:
                goods_dict['min_pic'] = image_obj.img_url

            goods_ls.append(goods_dict)
        return jsonify(errno=0, errmsg="OK", count=count, data=goods_ls)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品列表失败')


# PC商品详情
@api_goods.route('/pc_goods_detail', methods=['POST'])
@login_required
@admin_required
def pc_goods_detail():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            goods_id = int(goods_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        goods_obj = Goods.query.get(goods_id)
        if not goods_obj:
            return jsonify(errno=-1, errmsg='当前商品不存在')

        goods_ls = list()
        goods_dict = dict()
        goods_dict['name'] = goods_obj.name
        goods_dict['postage'] = goods_obj.postage
        goods_dict['price'] = goods_obj.price
        goods_dict['ku_num'] = goods_obj.ku_num
        goods_dict['available_num'] = goods_obj.available_num
        goods_dict['change_num'] = int(goods_obj.ku_num) - int(goods_obj.available_num)
        goods_dict['detail'] = goods_obj.detail
        # goods_dict['img_url'] = goods_obj.img_url

        # 当前商品的轮播图片
        images = GoodsImage.query.filter(GoodsImage.goods_id == goods_id).order_by(GoodsImage.is_min.desc()).all()
        image_list = list()
        for image in images:
            image_dict = dict()
            image_dict['img_id'] = image.id
            image_dict['img_url'] = image.img_url
            image_dict['is_min'] = image.is_min
            image_list.append(image_dict)
        goods_dict['image_data'] = image_list

        goods_ls.append(goods_dict)
        return jsonify(errno=0, errmsg="OK", data=goods_ls)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品详情失败')


# PC--当前商品已下单的用户信息
@api_goods.route('/goods_user_info', methods=['POST'])
def goods_user_info():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))

        try:
            goods_id = int(goods_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        goods_obj = Goods.query.get(goods_id)
        if not goods_obj:
            return jsonify(errno=-1, errmsg='当前商品不存在')

        orders = GoodsOrder.query.filter_by(goods_id=goods_id).paginate(page, pagesize, False)
        count = orders.total
        user_ls = list()
        if count != 0:
            location = 1
            for order in orders.items:
                user_id = order.user_id
                user = User.query.get(user_id)
                user_data = dict(
                    nick_name=base64.b64decode(user.nick_nameemoj),
                    avatar_url=user.avatar_url,
                    goods_name=goods_obj.name,
                    order_status=order.order_status,
                    create_time=str(order.create_time),
                    location=location
                )
                location += 1
                user_ls.append(user_data)

        return jsonify(errno=0, errmsg="OK", data=user_ls, count=count)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品详情失败')


# PC上架/下架
@api_goods.route('/goods_down', methods=['POST'])
@login_required
@admin_required
def down_line():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            goods_id = int(goods_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='goods_id错误')

        goods_obj = Goods.query.get(goods_id)
        if not goods_obj:
            return jsonify(errno=-1, errmsg='当前商品不存在')

        if goods_obj.is_show == 1:
            # 下架
            goods_obj.is_show = -1
        else:
            # 上架
            goods_obj.is_show = 1

        db.session.add(goods_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
    return jsonify(errno=-1, errmsg='修改商品状态失败')


# PC删除商品
@api_goods.route('/goods_del', methods=['POST'])
@login_required
@admin_required
def goods_del():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            goods_id = int(goods_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        goods_obj = Goods.query.get(goods_id)
        if not goods_obj:
            return jsonify(errno=-1, errmsg='当前商品不存在')

        order_obj = GoodsOrder.query.filter(GoodsOrder.goods_id == goods_id).first()
        if order_obj:
            return jsonify(errno=-1, errmsg='该商品已有人兑换不能删除')

        images = GoodsImage.query.filter(GoodsImage.goods_id == goods_id).all()
        for img in images:
            db.session.delete(img)

        db.session.delete(goods_obj)
        db.session.commit()
        return jsonify(errno=0, errmsg="OK")
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        db.session.rollback()
        return jsonify(errno=-1, errmsg='删除商品失败')


# 小程序--商品列表
@api_goods.route('/goods_list', methods=['POST'])
@auth_required
def goods_list():
    try:
        res = request.get_json()
        page = res.get('page', 1)
        pagesize = res.get('pagesize', 10)

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            page = int(page)
            pagesize = int(pagesize)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            page, pagesize = 1, 10

        results = Goods.query.filter(Goods.is_show == 1).order_by(Goods.create_time.desc()).paginate(page, pagesize,
                                                                                                     False)
        count = results.total

        goods_ls = list()
        for goods_obj in results.items:
            goods_dict = dict()
            goods_dict['goods_id'] = goods_obj.id
            goods_dict['goods_name'] = goods_obj.name
            goods_dict['price'] = goods_obj.price
            goods_dict['ku_num'] = goods_obj.ku_num  # 库存
            goods_dict['available_num'] = goods_obj.available_num  # 剩余可用库存
            goods_dict['change_num'] = int(goods_obj.ku_num) - int(goods_obj.available_num)  # 已兑换数量
            goods_dict['create_time'] = str(goods_obj.create_time)
            goods_dict['is_show'] = goods_obj.is_show
            goods_dict['postage'] = goods_obj.postage
            # goods_dict['img_url'] = goods_obj.img_url

            # # 当前商品的主图
            image_obj = GoodsImage.query.filter(GoodsImage.goods_id == goods_obj.id, GoodsImage.is_min == 1).first()
            if image_obj:
                goods_dict['min_pic'] = image_obj.img_url

            goods_ls.append(goods_dict)
        return jsonify(errno=0, errmsg="OK", count=count, data=goods_ls)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品列表失败')


# 小程序--商品详情
@api_goods.route('/goods_detail', methods=['POST'])
@auth_required
def goods_detail():
    try:
        res = request.get_json()
        goods_id = res.get('goods_id')

        Logging.logger.info('request_args:{0}'.format(res))
        try:
            goods_id = int(goods_id)
        except Exception as e:
            Logging.logger.error('errmsg:{0}'.format(e))
            return jsonify(errno=-1, errmsg='参数错误')

        goods_obj = Goods.query.get(goods_id)
        if not goods_obj:
            return jsonify(errno=-1, errmsg='当前商品不存在')

        goods_ls = list()
        goods_dict = dict()
        goods_dict['goods_id'] = goods_obj.id
        goods_dict['name'] = goods_obj.name
        goods_dict['postage'] = goods_obj.postage
        goods_dict['price'] = goods_obj.price
        goods_dict['ku_num'] = goods_obj.ku_num
        goods_dict['available_num'] = goods_obj.available_num
        goods_dict['change_num'] = int(goods_obj.ku_num) - int(goods_obj.available_num)
        goods_dict['detail'] = goods_obj.detail
        goods_dict['is_show'] = goods_obj.is_show

        # 当前商品的图片
        # images = GoodsImage.query.filter(GoodsImage.goods_id == goods_id).order_by(GoodsImage.is_min.desc()).all()
        images = GoodsImage.query.filter(GoodsImage.goods_id == goods_id).order_by(GoodsImage.create_time.asc()).all()
        image_list = list()
        for image in images:
            image_dict = dict()
            image_dict['img_id'] = image.id
            image_dict['img_url'] = image.img_url
            image_dict['is_min'] = image.is_min
            image_list.append(image_dict)
        goods_dict['image_data'] = image_list

        goods_ls.append(goods_dict)
        return jsonify(errno=0, errmsg="OK", data=goods_ls)
    except Exception as e:
        Logging.logger.error('errmsg:{0}'.format(e))
        return jsonify(errno=-1, errmsg='查询商品详情失败')
