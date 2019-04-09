from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

__all__ = ['Account', 'Course', 'Degree', 'CourseDetail', 'CourseOutline', 'CourseChapter',
           'CourseLesson', 'Teacher', 'Coupon', 'CouponDetail', 'Category',
           'CommonQuestion', 'Comment', 'Order', 'OrderDetail', 'PricePolicy', 'TradeRecord'
           ]


class Category(models.Model):
    """课程分类表"""
    title = models.CharField(max_length=32, verbose_name='课程分类名')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = 'DB_Category'
        db_table = verbose_name_plural


class Course(models.Model):
    """课程表"""
    title = models.CharField(max_length=32, verbose_name='课程标题')
    course_img = models.ImageField(verbose_name='课程图片', null=True, blank=True, upload_to='course/%Y-%m')
    status_choices = ((0, '预售中'), (1, '开设中'), (2, '已下架'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name='课程状态')
    difficult_choices = ((0, '初级'), (1, '中级'), (2, '高级'))
    difficult = models.SmallIntegerField(choices=difficult_choices, verbose_name='课程难度',
                                         default=0)
    course_type_choices = ((0, '付费'), (1, '免费'), (2, 'VIP专享'), (3, '学位课程'))
    course_type = models.SmallIntegerField(choices=course_type_choices, verbose_name='课程类型')
    release_date = models.DateField(verbose_name='发布日期', blank=True, null=True)
    order = models.IntegerField(verbose_name='课程顺序', help_text='从上一个课程开始')
    category = models.ForeignKey(to=Category, on_delete='cascade')
    study_number = models.IntegerField(verbose_name='学习人数', help_text='只要有人买，立即更新该字段')
    degree_course = models.ForeignKey(to='Degree', on_delete='cascade', help_text='如果是学位课程，必须关联学位表',
                                      blank=True, null=True)
    price_policy = GenericRelation(to='PricePolicy')
    common_question = GenericRelation(to='CommonQuestion')
    comment = GenericRelation(to='Comment')
    order_detail = GenericRelation(to='OrderDetail', related_name='courses')
    coupon = GenericRelation(to='Coupon')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = 'DB_Course'
        db_table = verbose_name_plural

    def save(self, *args, **kwargs):
        """做学位课程判断"""
        if self.course_type == 3:
            if not self.degree_course:
                raise ValueError('学位课程必须关联学位课程表')
        super(Course, self).save(*args, **kwargs)


class CourseDetail(models.Model):
    """课程详情表"""
    course = models.OneToOneField(to='Course', on_delete='cascade')
    lesson = models.IntegerField(default=7, verbose_name='总课时')
    slogan = models.CharField(max_length=64, verbose_name='课程口号', blank=True, null=True)
    brief = models.CharField(max_length=128, verbose_name='简介')
    why_study = models.CharField(max_length=1024, verbose_name='为什么学习')
    point = models.CharField(max_length=512, verbose_name='课程安排，能学到的知识点')
    harvest = models.CharField(max_length=1024, verbose_name='学完对我的职业生涯影响')
    feature = models.CharField(max_length=512, verbose_name='课程特点')
    prerequisite = models.TextField(max_length=1024, verbose_name='课程先修条件')
    object_person = models.CharField(max_length=128, verbose_name='面向人群')
    teacher = models.ManyToManyField(to='Teacher', verbose_name='授课讲师')
    recommend_course = models.ManyToManyField(to='Course', related_name='recommend_by',
                                              verbose_name='推荐课程')

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = '课程详情'
        verbose_name_plural = 'DB_CourseDetail'
        db_table = verbose_name_plural


class CourseOutline(models.Model):
    """课程大纲表"""
    course_detail = models.ForeignKey(to='CourseDetail', on_delete='cascade', related_name='course_outline')
    title = models.CharField(max_length=128, verbose_name='大纲名')
    order = models.SmallIntegerField(default=1, verbose_name='大纲顺序')
    content = models.TextField(max_length=2048, verbose_name='大纲内容')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程大纲'
        verbose_name_plural = 'DB_CourseOutline'
        db_table = verbose_name_plural
        unique_together = ('title', 'course_detail')  # 大纲名和课程详情做联合唯一


class CourseChapter(models.Model):
    """课程章节表"""
    course = models.ForeignKey(to='Course', on_delete='cascade', related_name='course_chapters')
    chapter = models.SmallIntegerField(default=1, verbose_name='第几章')
    title = models.CharField(max_length=32, verbose_name='章节名称')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = 'DB_CourseChapter'
        db_table = verbose_name_plural
        unique_together = ('chapter', 'course')  # 章节和课程联合唯一，一个课程不能有多个相同章节


class Degree(models.Model):
    """学位课程表"""
    title = models.CharField(max_length=32, verbose_name='学位课程名')
    aims = models.CharField(max_length=1024, verbose_name='培养目标')
    core = models.CharField(max_length=1024, verbose_name='核心优势')
    serving = models.CharField(max_length=1024, verbose_name='特色服务')
    price = models.ForeignKey(to='PricePolicy', verbose_name='价格', on_delete='cascade')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '学位表'
        verbose_name_plural = 'DB_Degree'
        db_table = verbose_name_plural


class CourseLesson(models.Model):
    """课时表"""
    chapter = models.ForeignKey(to='CourseChapter', verbose_name='课程章节', on_delete='cascade',
                                related_name='course_lesson')
    title = models.CharField(max_length=32, verbose_name='课时名称')
    order = models.SmallIntegerField(verbose_name='课时顺序', help_text='每三个隔开排序，方便以后更新课程插入')
    course_lesson_type_choices = ((0, '视频'), (1, '文档'), (2, '练习题'))
    course_lesson_type = models.SmallIntegerField(choices=course_lesson_type_choices,
                                                  verbose_name='课时类型', default=0)
    free_trail = models.BooleanField(verbose_name='是否可试看', default=False)
    lesson_link = models.CharField(max_length=255, verbose_name='课程链接', help_text='如果是文档，需要给链接',
                                   blank=True, null=True)

    def course_chapter(self):
        """快捷取出章节名"""
        return self.chapter.title

    def course_name(self):
        """快捷取出课程名"""
        return self.chapter.course.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课时'
        verbose_name_plural = 'DB_CourseLesson'
        db_table = verbose_name_plural
        unique_together = ('chapter', 'lesson_link')  # 课程章节和课时链接作联合唯一


class CommonQuestion(models.Model):
    """常见问题表"""
    content_type = models.ForeignKey(to=ContentType, on_delete='cascade')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    question = models.CharField(max_length=64, verbose_name='问题')
    answer = models.CharField(max_length=512, verbose_name='答案')

    def __str__(self):
        return '%s - %s' % (self.question, self.answer)

    class Meta:
        verbose_name = '常见问题'
        verbose_name_plural = 'DB_CommonQuestion'
        db_table = verbose_name_plural
        unique_together = ('content_type', 'object_id', 'question')


class Comment(models.Model):
    """评论表"""
    content_type = models.ForeignKey(to=ContentType, on_delete='cascade', null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    account = models.ForeignKey(to='Account', on_delete='cascade', verbose_name='评论用户')
    comment_date = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=1024, verbose_name='评论内容')

    def __str__(self):
        return '%s - %s - %s' % (self.account, self.comment_date, self.content)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = 'DB_Comment'
        db_table = verbose_name_plural


class Teacher(models.Model):
    """讲师表"""
    username = models.CharField(max_length=32, verbose_name='讲师姓名')
    title = models.CharField(max_length=64, verbose_name='讲师头衔')
    teacher_img = models.ImageField(upload_to='teacher/', null=True, blank=True, verbose_name='头像')
    brief = models.CharField(max_length=128, verbose_name='讲师简介')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '讲师表'
        verbose_name_plural = 'DB_Teacher'
        db_table = verbose_name_plural


# class Tutor(models.Model):
#     """导师表"""
#     username = models.CharField(max_length=32, verbose_name='导师姓名')
#     passwd = models.CharField(max_length=32, verbose_name='密码')
#     title = models.CharField(max_length=64, verbose_name='导师头衔')
#
#     def __str__(self):
#         return self.username


class Account(models.Model):
    """用户表"""
    username = models.CharField(max_length=32, verbose_name='用户名')
    passwd = models.CharField(max_length=32, verbose_name='密码')
    brief = models.CharField(max_length=64, verbose_name='学员简介')
    CHOICES = ((0, '大专'), (1, '本科'), (2, '研究生'), (3, '博士'), (4, '硕士'), (5, '其他'))
    education = models.IntegerField(choices=CHOICES, default=5, verbose_name='学历')
    career = models.CharField(max_length=32, verbose_name='目前职业/最近一次从事职业')
    balance = models.IntegerField(verbose_name='账户余额', default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = 'DB_Account'
        db_table = verbose_name_plural


class Coupon(models.Model):
    """优惠券表"""
    title = models.CharField(max_length=64, verbose_name='活动名')
    brief = models.TextField(max_length=128, verbose_name='优惠券介绍', blank=True, null=True)
    coupon_type_choices = ((0, '通用券'), (1, '抵扣券'), (2, '满减券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=0, help_text='通用券为全局优惠券，其他则为专项券')
    count = models.IntegerField(verbose_name='优惠券张数，发放一次立即更新该字段')
    equal_money = models.IntegerField(verbose_name='优惠券等值货币', blank=True, null=True, default=0)
    off_percent = models.PositiveIntegerField(verbose_name='折扣券百分比', blank=True, null=True, default=100,
                                              help_text='仅在折扣券使用')
    minimum_consume = models.FloatField(verbose_name='最低消费', blank=True, null=True, default=0,
                                        help_text='仅在满减券使用')

    grant_begin_time = models.DateTimeField(verbose_name='活动领取开始时间')
    grant_end_time = models.DateTimeField(verbose_name='活动领取结束时间')
    start_time = models.DateTimeField(verbose_name='优惠券有效期开始时间', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='优惠券有效期结束时间', blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name='优惠券有效期(天)', blank=True, null=True, default=0)

    date = models.DateTimeField(verbose_name='生效时间', help_text='即用户实际领取优惠券生效的时间', auto_now_add=True)

    content_type = models.ForeignKey(to=ContentType, on_delete='cascade', null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name='绑定的课程对象', null=True, blank=True,
                                            help_text='有值代表专项优惠券，没有值代表通用券')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '%s(%s)' % (self.title, self.get_coupon_type_display())

    class Meta:
        verbose_name = '优惠券规则'
        verbose_name_plural = 'DB_Coupon'
        db_table = verbose_name_plural

    def save(self, *args, **kwargs):
        """检测时间类型的字段"""
        if self.grant_begin_time >= self.grant_end_time:
            raise ValueError('活动开始时间不能大于等于活动结束时间')
        if not self.period or (self.start_time and self.end_time):
            if self.period == 0:
                raise ValueError('有效期时间不能为0')
            elif self.start_time >= self.end_time:
                raise ValueError('有效期开始时间能大于等于有效期结束时间')
        super(Coupon, self).save(*args, **kwargs)


class CouponDetail(models.Model):
    """优惠券详情表"""
    coupon = models.ForeignKey(to='Coupon', on_delete='cascade')
    number = models.CharField(max_length=64, unique=True, verbose_name='优惠券流水记录')
    account = models.ForeignKey(to='Account', verbose_name='优惠券拥有者', on_delete='cascade')
    status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    get_time = models.DateTimeField(verbose_name='用户领取时间')
    use_time = models.DateTimeField(verbose_name='用户使用时间', blank=True, null=True)
    order = models.ForeignKey(to='Order', on_delete='cascade', blank=True, null=True, verbose_name='关联订单',
                              help_text='一个订单可以有多个优惠券使用记录')

    class Meta:
        verbose_name = "用户优惠券领取使用记录表"
        verbose_name_plural = 'DB_CouponDetail'
        db_table = verbose_name_plural

    def __str__(self):
        return '%s-%s-%s' % (self.account, self.number, self.status)


class PricePolicy(models.Model):
    """价格策略表"""
    content_type = models.ForeignKey(to=ContentType, on_delete='cascade')
    object_id = models.PositiveIntegerField(verbose_name='课程对象')
    content_object = GenericForeignKey('content_type', 'object_id')
    valid_period_choices = ((1, '1天'), (3, '3天'),
                            (7, '1周'), (14, '2周'),
                            (30, '1个月'), (60, '2个月'),
                            (90, '3个月'), (120, '4个月'),
                            (180, '6个月'), (210, '12个月'),
                            (540, '18个月'), (720, '24个月'),
                            (722, '24个月'), (723, '24个月'),
                            )
    valid_period = models.SmallIntegerField(choices=valid_period_choices, verbose_name='课程有效期')
    price = models.FloatField(verbose_name='课程价格')

    def __str__(self):
        return "%s(%s) - %s" % (self.content_object, self.get_valid_period_display(), self.price)

    class Meta:
        verbose_name = '价格策略表'
        verbose_name_plural = 'DB_PricePolicy'
        db_table = verbose_name_plural


class Order(models.Model):
    """订单表"""
    payment_type_choices = ((0, '支付宝'), (1, '微信'), (2, '余额支付'), (3, '优惠吗'), (4, '银行卡支付'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices, verbose_name='付款类型')
    payment_number = models.IntegerField(verbose_name='支付第三方流水号', null=True, blank=True)
    order_nubmer = models.CharField(max_length=128, verbose_name='订单号', blank=True, null=True)
    account = models.ForeignKey(to='Account', verbose_name='下单用户', on_delete='cascade')
    payment_amount = models.FloatField(verbose_name='实付金额')
    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="订单状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")

    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = "DB_Order"
        db_table = verbose_name_plural

    def __str__(self):
        return "%s" % self.order_nubmer


class OrderDetail(models.Model):
    """订单详情表"""
    order = models.ForeignKey(to="Order", on_delete='cascade')
    original_price = models.FloatField(verbose_name="课程原价")
    price = models.FloatField(verbose_name="折后价格")
    valid_period_display = models.CharField(verbose_name="有效期在订单页显示", max_length=32,null=True,blank=True)
    valid_period = models.PositiveIntegerField(verbose_name="课程有效期(days)")
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name="订单交易备注")
    content_type = models.ForeignKey(ContentType, on_delete='cascade', verbose_name='关联普通课程或学位')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s - %s - %s" % (self.order, self.content_type, self.price)

    class Meta:
        verbose_name = '订单详细'
        verbose_name_plural = "DB_OrderDetail"
        db_table = verbose_name_plural


class TradeRecord(models.Model):
    """余额交易记录表"""
    account = models.ForeignKey(to=Account, on_delete='cascade', verbose_name='用户')
    amount = models.FloatField(verbose_name="交易金额")
    balance = models.FloatField(verbose_name="账户余额")
    transaction_type_choices = ((0, '收入'), (1, '支出'), (2, '退款'), (3, "提现"))  # 2 为了处理订单过期未支付时，锁定其余额的回退
    transaction_type = models.SmallIntegerField(choices=transaction_type_choices, verbose_name='交易类型')
    transaction_number = models.CharField(unique=True, verbose_name="流水号", max_length=128)
    date = models.DateTimeField(auto_now_add=True, verbose_name='交易时间')
    product = models.CharField(max_length=2048, verbose_name='商品名',
                               null=True, blank=True,
                               help_text='如果是支出和退款一定写入购买的商品')
    user_address = models.CharField(max_length=512, verbose_name='收获地址', null=True, blank=True)
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name="交易备注")

    class Meta:
        verbose_name = '余额交易记录'
        verbose_name_plural = "DB_TradeRecord"
        db_table = verbose_name_plural

    def __str__(self):
        return "%s" % self.transaction_number

    def save(self, *args, **kwargs):
        if self.transaction_type not in [1, 2]:
            if self.product:
                raise ValueError('支出和退款必须写入购买退款的商品名')
        super(TradeRecord, self).save(*args, **kwargs)
