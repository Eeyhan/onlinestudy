from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from generic import serializers
from generic import models
from django.db.models import F
from utils.Auther import Auther
from utils.redis_pool import POOL
from utils.BaseResponse import BaseResponse
import redis
import json
import time
from collections import OrderedDict


# Create your views here.


class CategoryView(APIView):
    """课程分类"""

    def get(self, request):
        category = models.Category.objects.all()
        res = serializers.CategorySerializer(category, many=True)
        return Response(res.data)


class CourseView(APIView):
    """课程"""

    def get(self, request):
        cid = request.query_params.get('cid')
        query = request.query_params.get('query')
        if cid:
            cid = eval(cid)
        # 是否有课程分类id
        if cid == 0:
            course = models.Course.objects.all()
            course = self.order_query(query, course)
        else:
            course = models.Course.objects.filter(category_id=cid).all().order_by('category_id')
            course = self.order_query(query, course)
        res = serializers.CourseSerializer(course, many=True)

        # 针对mysql数据库数据去重
        if query:
            temp = res.data
            temp.clear()
            for item in res.data:
                if item not in temp:
                    temp.append(item)
                else:
                    continue
            return Response(temp)
        return Response(res.data)

    def order_query(self, query, course):
        """mysql对distinct不能加参数"""
        if query:
            if query == 'hot':
                course = course.order_by('-study_number')
            elif query == 'price':
                course = course.order_by('price_policy__price').distinct()  # 跨表排序升序

            elif query == '-price':
                course = course.order_by('price_policy__price').distinct()  # 跨表排序降序
                course = course.reverse()
                # 拆分去重代码
        return course


class DegreeView(APIView):
    """课程"""

    def get(self, request):
        course = models.Course.objects.filter(degree_course__isnull=False).all().order_by('category_id')
        res = serializers.CourseSerializer(course, many=True)
        return Response(res.data)


class CourseDetailView(APIView):
    """课程详情"""

    def get(self, request, pk):
        courseDetail = models.CourseDetail.objects.filter(course_id=pk)
        # courseDetail = models.CourseDetail.objects.all()
        res = serializers.CourseDetailSerializer(courseDetail, many=True)
        return Response(res.data)


class CourseChapterView(APIView):
    """课程章节，课时"""

    def get(self, request, pk):
        coursechapter = models.CourseChapter.objects.filter(course_id=pk).all().order_by('chapter')
        # coursechapter = models.CourseChapter.objects.all()
        res = serializers.ChapterSerializer(coursechapter, many=True)
        return Response(res.data)


class CourseCommentView(APIView):
    """课程评论"""

    def get(self, request, pk):
        # coursecomment = models.Comment.objects.filter(object_id=pk).first().content_object.comment.all()
        coursecomment = models.Course.objects.filter(id=pk).first().comment.all()
        res = serializers.CommentSerializer(coursecomment, many=True)
        return Response(res.data)


class CourseCommonquestionView(APIView):
    """课程常见问题"""

    def get(self, request, pk):
        # coursecomment = models.CommonQuestion.objects.filter(object_id=pk).first().content_object.common_question.all()
        commonquestion = models.Course.objects.filter(id=pk).first().common_question.all().order_by('id')
        res = serializers.CommonQuestionSerializer(commonquestion, many=True)
        return Response(res.data)


# ------------------ 购物车,结算相关 --------------------------|

SHOPPING_KEY = 'SHOPPING_%s_%s'
SETTLEMENT_KEY = "SETTLEMENT_%s_%s"
GLOBAL_COUPON_KEY = 'GLOBAL_COUPON_%s'
CONN = redis.Redis(connection_pool=POOL)


class ShoppingView(APIView):
    authentication_classes = [Auther, ]

    """
        与前端商量好的存入redis数据格式：
        {
            SHOPPINGCAR_USERID_COURSE_ID: {
                "id", 
                "title",
                "course_img",
                "price_policy_dict": {
                    price_policy_id: "{valid_period, valid_period_display, price}"
                    price_policy_id2: "{valid_period, valid_period_display, price}"
                    price_policy_id3: "{valid_period, valid_period_display, price}"        
                },
                "default_price_policy_id": 1       

            }
        }
    """

    # 购物车数据存到redis里

    def get(self, request):
        res = BaseResponse()
        # 从redis数据库中取出购物车的数据
        user_id = request.user.pk
        key = SHOPPING_KEY % (user_id, '*')
        # 找到跟当前用户相关的所有购物车数据的key
        all_keys = CONN.scan_iter(key)

        course_info = []
        for key in all_keys:
            course_info.append(CONN.hgetall(key))
        if len(course_info) == 0:
            res.data = '您的购物车空空如也哦~'
        else:
            res.data = course_info
        # 返回给前端
        return Response(res.dict)

    def post(self, request):
        res = BaseResponse()
        # 拿到前端传过来的数据
        course_id = request.data.get('course')
        price_policy_id = request.data.get('price_policy')
        user = request.user
        multi = request.data.get('multi')  # 传来多个课程参数

        # 检测数据合法
        try:
            # 这里可以判断是一个课程还是多个课程

            # 如果前端传来单个课程参数
            if not multi:
                # {"course": 1, "price_policy": 1}
                res = self.post_func(res, course_id, price_policy_id, user)
            # 如果前端传来多个课程参数
            else:
                for item in multi:
                    # {"multi":[{"course":2,"price_policy":10},{"course":3,"price_policy":4}]}
                    course = item['course']
                    price_policy = item['price_policy']
                    ret = self.post_func(res, course, price_policy, user)

        except Exception as e:
            print(e)
            res.code = 1042
            res.error = '操作失败，请重试'
            return Response(res.dict)
        else:
            res.data = '加入购物车成功'
            return Response(res.dict)

    def post_func(self, res, course_id, price_policy_id, user):
        # 加入购物车函数，通用部分
        course_obj = models.Course.objects.filter(id=course_id).first()
        if not course_obj:
            res.code = 1040
            res.error = '不存在该课程'
            return Response(res.dict)
        price_queryset = course_obj.price_policy.all()
        price_policy_dict = {}
        for price_policy in price_queryset:
            price_policy_dict[price_policy.id] = {
                'price': price_policy.price,
                'valid_period': price_policy.valid_period,
                'valid_period_display': price_policy.get_valid_period_display()

            }

        if price_policy_id not in price_policy_dict:
            res.code = 1041
            res.error = '课程价格不合法'
            return Response(res.dict)
        # redis的key
        key = SHOPPING_KEY % (user.id, course_id)

        # redis的课程key对应的数据
        # image类型和dict都需要处理一下才行，不然无法存入数据库
        course_info = {
            'id': course_obj.id,
            'title': course_obj.title,
            'course_img': str(course_obj.course_img),
            'price_policy_dict': json.dumps(price_policy_dict, ensure_ascii=False),
            'default_price_policy': price_policy_id
        }

        # 存入redis里面
        CONN.hmset(key, course_info)
        return res

    def put(self, request):
        res = BaseResponse()
        # 拿到前端传过来的新的数据  {"course": 1, "price_policy": 16}
        course_id = request.data.get('course')
        price_policy_id = request.data.get('price_policy')
        user = request.user
        # 检测是否有该课程
        course_obj = models.Course.objects.filter(id=course_id).first()
        if not course_obj:
            res.code = 1042
            res.error = '课程id不合法，不存在该课程'
        try:
            key = SHOPPING_KEY % (user.id, course_id)
            print(key)
            print(course_obj)
            if not CONN.exists(key):
                res.code = 1050
                res.error = '课程id不合法，购物车内没有该课程数据'
                return Response(res.dict)
            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict'))
            if str(price_policy_id) not in price_policy_dict:
                res.code = 1051
                res.error = '价格策略不合法'
                return Response(res.dict)
            CONN.hset(key, 'default_price_policy', price_policy_id)

        except Exception as e:
            print(e)
            res.code = 1052
            res.error = '操作失败，请重试'
            return Response(res.dict)
        else:
            res.data = '修改成功'
            return Response(res.dict)

    def delete(self, request):
        res = BaseResponse()
        # 拿到前端传过来的数据
        course_list = request.data.get('course')
        user = request.user

        # 检测是否有该课程
        try:
            # 如果前端传来的数据只有一个
            if not isinstance(course_list, list):
                res = self.delete_func(user, course_list, res)
            # 如果前端传来的数据有多个
            else:
                for course in course_list:
                    res = self.delete_func(user, course, res)
        except Exception as e:
            print(e)
            res.code = 1061
            res.error = '操作失败请重试'
            return Response(res.dict)
        else:
            res.data = '已删除选中课程'
            return Response(res.dict)

    def delete_func(self, user, course, res):
        # 删除函数，通用部分
        key = SHOPPING_KEY % (user.id, course)
        if not CONN.exists(key):
            res.code = 1060
            res.error = '选中课程不合法'
            return Response(res.dict)
        # 存在则删除
        CONN.delete(key)
        return res


class SettlementView(APIView):
    """结算"""
    authentication_classes = [Auther, ]

    def get(self, request):
        res = BaseResponse()
        # 获取redis里的数据
        user_id = request.user.pk
        key = SETTLEMENT_KEY % (user_id, '*')
        global_key = GLOBAL_COUPON_KEY % user_id
        user_settlement_keys = CONN.scan_iter(key)
        settlement_info = []
        for field in user_settlement_keys:
            settlement_info.append(CONN.hgetall(field))
        global_data = CONN.hgetall(global_key)

        res.data = {
            'settlement_info': settlement_info,
            'global_coupon_dict': global_data

        }
        return Response(res.dict)

        # 返回给前端展示

    def post(self, request):
        res = BaseResponse()
        # 拿到前端传来的课程id数据
        course_list = request.data.get('course_list')
        user = request.user
        try:
            for course_id in course_list:
                # 检验redis数据库里是否存在，如果存在取出对应优惠券
                key = SHOPPING_KEY % (user.id, course_id)
                if not CONN.exists(key):
                    res.code = 1070
                    res.error = '课程id不合法'
                    return Response(res.dict)
                user_coupons = models.CouponDetail.objects.filter(
                    account_id=user.id,
                    status=0,
                    coupon__start_time__lte=now(),
                    coupon__end_time__gte=now(),
                ).all()
                # 构建数据
                user_coupon_dict = {}
                user_global_coupon_dict = {}
                # 筛选优惠券是全局优惠券还是专项优惠券
                for coupon_record in user_coupons:
                    coupon = coupon_record.coupon
                    if coupon.object_id == course_id:  # 专项优惠券
                        user_coupon_dict[coupon.id] = {
                            'id': coupon.id,
                            'title': coupon.title,
                            'coupon_type': coupon.get_coupon_type_display(),
                            'equal_money': coupon.equal_money,
                            'off_percent': coupon.off_percent,
                            'minimum_consume': coupon.minimum_consume
                        }

                    elif coupon.object_id is None:  # 全局优惠券
                        user_global_coupon_dict[coupon.id] = {
                            'id': coupon.id,
                            'title': coupon.title,
                            'coupon_type': coupon.get_coupon_type_display(),
                            'equal_money': coupon.equal_money,
                            'off_percent': coupon.off_percent,
                            'minimum_consume': coupon.minimum_consume
                        }
                # 去购物车信息里取对应课程信息
                course_info = CONN.hgetall(key)
                # 拿到价格策略字典
                price_policy_dict = json.loads(course_info['price_policy_dict'])
                # 拿到默认选中价格策略
                default_price_policy_id = course_info['default_price_policy']
                # 拿到有效期
                valid_period = price_policy_dict[default_price_policy_id]['valid_period']
                # 拿到价格
                price = price_policy_dict[default_price_policy_id]['price']

                settlement_info = {
                    'id': course_info['id'],
                    'title': course_info['title'],
                    'course_img': course_info['course_img'],
                    'price': price,
                    'valid_period': valid_period,
                    'course_coupon_dict': json.dumps(user_coupon_dict, ensure_ascii=False),
                }

                # 存入redis数据
                user_settlements = SETTLEMENT_KEY % (user.id, course_id)
                user_global_coupons = GLOBAL_COUPON_KEY % user.id
                CONN.hmset(user_settlements, settlement_info)

                if user_global_coupon_dict:
                    # 多套了一层，不然redis报错，不能内层直接套一个字典
                    global_settlement_info = {
                        'global_course_coupon_dict': json.dumps(user_global_coupon_dict, ensure_ascii=False)
                    }
                    CONN.hmset(user_global_coupons, global_settlement_info)

                # 删除购物车数据
                CONN.delete(key)
        except Exception as e:
            print(e)
            res.code = 1071
            res.error = '操作失败，请重试'
            return Response(res.dict)
        else:
            res.data = '加入结算中心成功'
            return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        # 获取前端传来的数据
        course_id = request.data.get('course')
        course_coupon_id = request.data.get('coupon')
        global_coupon_id = request.data.get('global_coupon')
        user_id = request.user.pk
        key = SETTLEMENT_KEY % (user_id, course_id)
        global_key = GLOBAL_COUPON_KEY % user_id
        # 验证数据合法
        if course_id:
            if not CONN.exists(key):
                res.code = 1080
                res.error = '课程id不合法'
                return Response(res.dict)
        if course_coupon_id:
            user_coupon_dict = json.loads(CONN.hget(key, 'course_coupon_dict'))
            if str(course_coupon_id) not in user_coupon_dict:
                res.code = 1081
                res.error = '课程优惠券id不合法'
                return Response(res.dict)
            CONN.hset(key, 'default_coupon_id', course_coupon_id)

        if global_coupon_id:
            if not CONN.exists(global_key):
                res.code = 1082
                res.error = '全局优惠券id不合法'
                return Response(res.dict)
            CONN.hset(global_key, 'default_global_coupon_id', global_coupon_id)
        res.data = '已选择优惠券'
        return Response(res.dict)

    def delete(self, request):
        """取消订单"""
        res = BaseResponse()
        user_id = request.user.pk
        course_list = request.data.get('course')
        if not isinstance(course_list, int):
            for course in course_list:
                res = self.delete_func(user_id, course, res)

        else:
            res = self.delete_func(user_id, course_list, res)
        res.data = '订单删除成功'
        return Response(res.dict)

    def delete_func(self, user_id, course, res):
        key = SETTLEMENT_KEY % (user_id, course)
        global_key = GLOBAL_COUPON_KEY % user_id
        if key:
            if not CONN.exists(key):
                res.code = 1090
                res.error = '课程id不合法'
                return Response(res.dict)
            CONN.delete(key)

        if global_key:
            if not CONN.exists(global_key):
                res.code = 1091
                res.error = '全局优惠券id不合法'
            CONN.delete(global_key)
        return res


class PaymentView(APIView):
    """支付接口"""
    authentication_classes = [Auther, ]

    def get(self, request):
        # 调用业务数据库的数据进行查看展示
        """

        账单详情：
        [
            账单id:{
                商品名：
                简介：
                数量：
                价格：
                图片：
            },
        ]

        创建订单时间：
        下单付款时间:
        流水号:
        付款方式:
        实付金额:
        收获地址：

        """

        res = BaseResponse()
        user_trades = models.TradeRecord.objects.filter(account=request.user).all()
        user_order = models.OrderDetail.objects.filter(order__account=request.user).all()

        pay_dict = {}
        # 商品数量
        order_menu = {}
        for order in user_order:
            order_menu[order.object_id] = {
                'real_price': order.price,
                'order_date': order.order.date,
                'pay_date': order.order.pay_time
            }

        for trade in user_trades:
            product = eval(trade.product)

            # print(product)
            pay_dict[trade.id] = {}
            for item in product:
                brief = models.Course.objects.filter(id=int(item['id'])).first().coursedetail.brief

                pay_dict[trade.id][item['id']] = item
                pay_dict[trade.id][item['id']]['brief'] = brief

                for order_id in order_menu:
                    if int(order_id) == int(item['id']):
                        pay_dict[trade.id][item['id']]['real_price'] = order_menu[order_id]['real_price']
                        pay_dict[trade.id]['order_date'] = order_menu[order_id]['order_date']
                        pay_dict[trade.id]['pay_date'] = order_menu[order_id]['pay_date']
                    res.data = pay_dict
            pay_dict[trade.id]['transaction_number'] = trade.transaction_number
            pay_dict[trade.id]['user_address'] = trade.user_address
            pay_dict[trade.id]['pay_success_time'] = trade.date

        return Response(res.dict)

    def post(self, request):
        res = BaseResponse()
        # 获取前端传来的数据
        # {"balance": 20, "price": 73.1}
        balance = request.data.get('balance')
        price = request.data.get('price')
        user = request.user
        if int(balance) > request.user.balance:
            res.code = 1100
            res.error = '抵扣贝里失败，贝里余额不足'
            return Response(res.dict)
        user_key = SETTLEMENT_KEY % (user.id, "*")
        user_settlements = CONN.scan_iter(user_key)

        total_price = 0
        user_coupon_dict = {}
        global_coupon_dict = {}
        for item in user_settlements:
            settlement_info = CONN.hgetall(item)
            course_id = settlement_info['id']
            # 检验课程合法性
            course_obj = models.Course.objects.filter(id=course_id).first()
            if not course_obj and course_obj.state == 2:  # 状态2表示课程下架
                res.code = 1101
                res.error = '课程id不正确，可能已下架'
                return Response(res.dict)
            course_coupon_id = int(settlement_info.get('default_coupon_id', 0))
            # 有优惠券，检验课程优惠券有效期
            if course_coupon_id:
                user_coupon_dict = models.Coupon.objects.filter(
                    id=course_coupon_id,
                    object_id=course_id,
                    start_time__lte=now(),
                    end_time__gte=now(),
                    coupondetail__account_id=user.id,
                    coupondetail__status=0).values('coupon_type', 'equal_money', 'off_percent', 'minimum_consume')

                if course_coupon_id and not user_coupon_dict:
                    res.code = 1102
                    res.error = '优惠券id不合法'
                    return Response(res.dict)

                course_db_price = settlement_info['price']
                course_count_price = self.counts(user_coupon_dict, course_db_price)
                if course_count_price == -1:
                    res.code = 1103
                    res.error = '优惠券不符合使用要求'
                    return Response(res.dict)
                total_price += course_count_price
                # 修改优惠券使用状态
                models.CouponDetail.objects.filter(account_id=user.id,
                                                   coupon__coupon_type__in=[1, 2]).update(status=1, use_time=now())

            # 没有优惠券的情况
            else:
                total_price += float(settlement_info['price'])

        # 全局优惠券
        # 有三个情况：
        #   1.当前用户本来就没有领取全局优惠券
        #   2.当前用户有全局优惠券但和redis里的数据不匹配
        #   3.正常使用优惠券
        # 判断用户是否有优惠券

        user_global_coupon = models.CouponDetail.objects.all().filter(account_id=user.id, coupon__coupon_type=0)

        # 有全局优惠券，检查优惠券使用场景合法性
        if user_global_coupon:
            global_coupon_key = GLOBAL_COUPON_KEY % user.id
            # 当前用户有全局优惠券但和redis里的数据不匹配，优惠券不可用，价格默认为之前的值
            if not CONN.exists(global_coupon_key):
                # 报一个警告
                res.code = 1104
                res.error = '全局优惠券当前不可用'
                global_count_price = total_price
                # return Response(res.dict)
            global_coupon_id = CONN.hget(global_coupon_key, 'default_global_coupon_id')
            if global_coupon_id:
                global_coupon_dict = models.Coupon.objects.filter(
                    id=global_coupon_id,
                    start_time__lte=now(),
                    end_time__gte=now(),
                    couponrecord__account_id=user.id,
                    couponrecord__status=0).values('coupon_type', 'equal_money', 'off_percent', 'minimum_consume')

                if not global_coupon_dict:
                    res.code = 1105
                    res.error = '全局优惠券不合法'
                    return Response(res.dict)
                global_count_price = self.counts(global_coupon_dict, total_price)
                if global_count_price == -1:
                    res.code = 1106
                    res.error = '全局优惠券不符合使用要求'
                    return Response(res.dict)
                # 修改优惠券使用状态
                models.CouponDetail.objects.filter(account_id=user.id, coupon__coupon_type=0).update(status=1)

        # 没有全局优惠券,最后的价格就是前面的专项优惠券打折之后的值
        else:
            global_count_price = total_price

        # 抵扣账户余额金币，按平台换算比例，1:100

        balance_equivalent = balance / 100  # balance是前端传来的数据
        total_price = global_count_price - balance_equivalent
        if total_price < 0:
            total_price = 0
        total_price = float('%.2f' % total_price)
        # 最后的检验
        if price != total_price:  # price是前端传来的总价格
            # 说明前端传来的数据不正确
            res.code = 1107
            res.error = '操作失败，数据可能被篡改'
            return Response(res.dict)

        # 调用支付接口

        res.data = '付款成功'

        # 更新业务数据库里的数据

        # 删掉redis结算中心里的数据

        # 不知道为什么这里又要再取一次才能删除
        user_key = SETTLEMENT_KEY % (user.id, "*")
        user_settlements = CONN.scan_iter(user_key)

        # 把课程数据从redis里删除并存入交易表中
        product = []
        for item in user_settlements:
            product.append(CONN.hgetall(item))
            CONN.delete(item)
        CONN.delete(global_coupon_key)  # 此处不用判断是否有优惠券，redis删除，如果没有值不会报错

        # 更新数据库信息
        user_obj = models.Account.objects.filter(id=user.id)
        user_obj.update(balance=F('balance') - balance)

        # 用余额交易
        models.TradeRecord.objects.create(account_id=user.id, amount=balance,
                                          transaction_type=1, balance=user_obj.first().balance,
                                          transaction_number='pay' + str(time.time()), product=product)
        # 用其他方式交易
        # 获取交易类型
        order_obj = models.Order.objects.create(payment_type=0, account_id=user.id, payment_amount=total_price,
                                                status=0, pay_time=now())

        for item in product:
            pay_course_obj = models.Course.objects.filter(id=item['id']).first()
            course_coupon_dict = json.loads(item['course_coupon_dict'])
            price = float('%.2f' % float(item['price']))  # 不失真的转为浮点型数据，并取两位小数
            # 如果有优惠券
            if len(course_coupon_dict) != 0:
                for key, value in course_coupon_dict.items():
                    real_price = price - value['equal_money']
                models.OrderDetail.objects.create(order=order_obj, original_price=item['price'],
                                                  price=real_price,
                                                  valid_period=item['valid_period'],
                                                  content_object=pay_course_obj)
            # 没有优惠券
            else:
                models.OrderDetail.objects.create(order=order_obj, original_price=item['price'],
                                                  price=price,
                                                  valid_period=item['valid_period'],
                                                  content_object=pay_course_obj)

        return Response(res.dict)

    def counts(self, user_coupon_dict, price):
        """结算价格总和"""
        user_coupon_dict = user_coupon_dict.first()
        price = float(price)
        coupon_type = user_coupon_dict['coupon_type']
        if coupon_type == 0:  # 满减券
            minimum_consume = user_coupon_dict['minimum_consume']
            equal_money = user_coupon_dict['equal_money']
            if minimum_consume > price:
                return -1
            else:
                result = price - equal_money
                return result
        elif coupon_type == 1:  # 折扣券
            off_percent = user_coupon_dict['off_percent'] / 100
            minimum_consume = user_coupon_dict['minimum_consume']
            if minimum_consume > price:
                print(minimum_consume, price)
                return -1
            else:
                result = price * off_percent
                return result
        elif coupon_type == 2:  # 通用券
            equal_money = user_coupon_dict['equal_money']
            if price - equal_money <= 0:
                return -1
            else:
                result = price - equal_money
            return result

    def put(self, request):
        # 退款,退货
        # 售后服务、纠纷
        # 评价
        # 追评
        pass

    def delete(self, request):
        """删除账单"""
        res = BaseResponse()
        orders = request.data.get('order')
        user = request.user
        if not isinstance(orders, int):
            for order_id in orders:
                res = self.delete_func(user, order_id, res)
        else:
            res = self.delete_func(user, orders, res)
        res.data = '账单删除成功'
        return Response(res.dict)

    def delete_func(self, user, orders, res):
        # models.OrderDetail.objects.filter(order__account=user).all().filter(order_id=orders).delete()
        models.TradeRecord.objects.filter(account=user).all().filter()
        # print(tet)
        return res


class CouponDistributionView(APIView):
    authentication_classes = [Auther, ]
    """优惠券发放接口"""

    # 优惠券对于用户来说只有查看和获取的功能

    def get(self, request):
        """查看优惠券"""
        res = BaseResponse()
        all_coupon = models.Coupon.objects.all()
        coupon_dict = {}
        for item in all_coupon:
            coupon_dict[item.id] = {
                'id': item.id,
                'title': item.title,
                'brief': item.brief,
                'coupon_type': item.coupon_type,
                'coupon_type_display': item.get_coupon_type_display(),
                'grant_begin_time': item.grant_begin_time,
                'grant_end_time': item.grant_end_time,
                'start_time': item.start_time,
                'end_time': item.end_time,
                'period': item.date
            }
        res.data = coupon_dict
        return Response(res.dict)

    def post(self, request):
        """领取优惠券"""
        res = BaseResponse()
        # 优惠券只能一个一个领取，所以不考虑多个操作
        coupon_id = request.data.get('coupon')
        # 检查数据合法性
        coupon_obj = models.Coupon.objects.filter(id=coupon_id).first()
        if not coupon_obj:
            res.code = 1108
            res.error = '优惠券id不合法'
            return Response(res.dict)

        models.Coupon.objects.filter(id=coupon_id).update(count=F('count') - 1)
        models.CouponDetail.objects.create(coupon=coupon_obj, number=str(time.time()),
                                           account=request.user, get_time=now())

        res.data = '优惠券领取成功'
        return Response(res.dict)
