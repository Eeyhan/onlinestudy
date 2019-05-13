from django.test import TestCase
from generic import models


# Create your tests here.

class TestGeneric(TestCase):
    """测试model表数据"""

    def setUp(self):
        cate_obj = models.Category.objects.create(title='云计算')

        course_obj = models.Course.objects.create(title='云计算一个月入门', course_type=0, order=40, category=cate_obj,
                                                  status=1, study_number=88)
        price_obj = models.PricePolicy.objects.create(content_object=course_obj, valid_period=30, price=20)
        course_detail_obj = models.CourseDetail.objects.create(course=course_obj, lesson=90, brief='带你走进云计算的世界',
                                                               why_study='当今社会，已经离不开云计算', point='test',
                                                               harvest='踏入云计算的大门', feature='test', prerequisite='零门槛',
                                                               object_person='社会人员')
        course_outline_obj = models.CourseOutline.objects.create(course_detail=course_detail_obj, title='什么是云计算',
                                                                 order=1, content='云计算简介，入门')
        course_chapter_obj = models.CourseChapter.objects.create(course=course_obj, chapter=1, title='第一章-云计算入门学习')
        course_lesson_obj = models.CourseLesson.objects.create(chapter=course_chapter_obj, title='计算机发展史，云计算', order=1)

        common_question_obj = models.CommonQuestion.objects.create(question='云计算是否还有市场', answer='目前还在发展势头阶段',
                                                                   content_object=course_obj)
        account_obj = models.Account.objects.create(brief='test', education=1, username='雯雯', passwd=123456,
                                                    email='1014841000@qq.com')
        comment_obj = models.Comment.objects.create(account=account_obj, content='不错不错', content_object=course_obj)

        teacher_obj = models.Teacher.objects.create(username='jack', title='test', brief='test')
        coupon_obj = models.Coupon.objects.create(title='测试优惠券', grant_begin_time='2019-05-08',
                                                  grant_end_time='2019-09-08', period=180, count=999)

        order_obj = models.Order.objects.create(payment_type=1, payment_number=1651115651561665,
                                                order_nubmer='pay411616115615', account=account_obj, payment_amount=20,
                                                status=0, pay_time='2019-5-10')
        order_detail_obj = models.OrderDetail.objects.create(order=order_obj, content_object=course_obj, price=20)
        coupon_detail_obj = models.CouponDetail.objects.create(coupon=coupon_obj, number='pay4161safdaswetest',
                                                               account=account_obj, get_time='2019-05-08',
                                                               order=order_obj)

        trade_order_obj = models.TradeRecord.objects.create(account=account_obj, order=order_obj, amount=0, balance=0, )
        tutor_account_obj = models.Account.objects.create(brief='test', education=2, username='刘文', passwd=123456,
                                                          level=1, email='101012021@qq.com')
        tutor_obj = models.Tutor.objects.create(account=tutor_account_obj)
        student_obj = models.Student.objects.create(account=account_obj, student_status=2, tutor=tutor_obj)
        student_obj.courses.add(course_obj)
        admin_account_obj = models.Account.objects.create(brief='test', education=2, username='adminpink',
                                                          passwd=123456,
                                                          email='101098742@qq.com')
        admin_obj = models.Admins.objects.create(account=admin_account_obj)
        payment_record_obj = models.PaymentRecord.objects.create(account=account_obj, course=course_obj,
                                                                 confirm_status=2)
        consult_record_obj = models.ConsultRecord.objects.create(student=account_obj, consultant=tutor_obj,
                                                                 note='testss')
        score_obj = models.ScoreRecord.objects.create(student=account_obj, content='testtestset', score=20,
                                                      user=tutor_obj)
        study_question_obj = models.StudyQuestion.objects.create(student=account_obj, tutor=tutor_obj,
                                                                 question='XX怎么配置的',
                                                                 answer='先这样，再这样，就行了', answer_date='2019-05-10')
        homework_obj = models.Homework.objects.create(content='testsetsetst', title='完成XX配置')
        homework_obj.courses.add(course_obj)
        homework_obj.chapter.add(course_chapter_obj)
        homework_detail_obj = models.HomeworkDetail.objects.create(homework=homework_obj)
        homework_detail_obj.student.add(student_obj)
        homework_detail_obj.teacher.add(tutor_obj)

        article_obj = models.Article.objects.create(title='test一下', content='jaiojfioasjfioajewhfiuowa')
        study_record_obj = models.StudyRecord.objects.create(status=1)
        study_record_obj.student.add(student_obj)
        study_record_obj.course_lesson.add(course_lesson_obj)

    def test_isqual(self):
        course = models.Course.objects.get(title='云计算一个月入门')
        self.assertEqual(course.category.title, '云计算')

        prices = models.PricePolicy.objects.filter(price=20, object_id=course.id).all()
        for item in course.price_policy.all():
            for price_obj in prices:
                self.assertEqual(price_obj, item)

        course_detail = course.coursedetail
        self.assertEqual(course_detail.brief, '带你走进云计算的世界')

        course_outline = models.CourseOutline.objects.filter(course_detail=course_detail).first()
        self.assertEqual(course_outline.title, '什么是云计算')

        course_chapter = models.CourseChapter.objects.filter(course=course).first()
        self.assertEqual(course_chapter.title, '第一章-云计算入门学习')

        course_lesson = models.CourseLesson.objects.filter(chapter=course_chapter).first()
        self.assertIn(course_lesson.title, '计算机发展史，云计算')

        account = models.Account.objects.get(username='雯雯')
        self.assertEqual(account.brief, 'test')

        teacher = models.Teacher.objects.get(username='jack')
        self.assertEqual(teacher.brief, 'test')

        tutor = models.Tutor.objects.get(account__username='刘文')
        self.assertEqual(tutor.account.brief, 'test')

        student = models.Student.objects.get(account=account)
        self.assertEqual(student.account.email, '1014841000@qq.com')

        admins = models.Admins.objects.get(account__username='adminpink')
        self.assertEqual(admins.account.brief, 'test')

        article = models.Article.objects.get(title='test一下')
        self.assertEqual(article.content, 'jaiojfioasjfioajewhfiuowa')

        commont_questions = models.CommonQuestion.objects.filter(object_id=course.id).all()
        for item in course.common_question.all():
            for question in commont_questions:
                self.assertEqual(question, item)

        comments = models.Comment.objects.filter(object_id=course.id).all()
        for item in course.comment.all():
            for comment in comments:
                self.assertEqual(comment, item)

        coupons = models.Coupon.objects.filter(object_id=course.id).all()
        for item in course.coupon.all():
            for coupon in coupons:
                coupon_detail = models.CouponDetail.objects.filter(coupon=coupon, account=account).first()

                self.assertEqual(coupon_detail.get_time, '2019-05-08')
                self.assertEqual(coupon, item)

        order = models.Order.objects.get(order_nubmer='pay411616115615')
        self.assertEqual(order.payment_amount, 20)

        order_detail = models.OrderDetail.objects.filter(order=order).first()
        self.assertEqual(order_detail.price, 20)

        trade_record = models.TradeRecord.objects.filter(order=order).first()
        self.assertEqual(trade_record.account.username, '雯雯')

        payment_record = models.PaymentRecord.objects.filter(account=account).first()
        self.assertEqual(payment_record.confirm_status, 2)

        consult_record = models.ConsultRecord.objects.filter(note='testss').first()
        self.assertEqual(consult_record.student, account)

        score = models.ScoreRecord.objects.filter(content='testtestset').first()
        self.assertEqual(score.score, 20)

        study_question = models.StudyQuestion.objects.filter(question='XX怎么配置的').first()
        self.assertEqual(study_question.answer, '先这样，再这样，就行了')

        homework = models.Homework.objects.get(content='testsetsetst')
        self.assertEqual(homework.title, '完成XX配置')

        homework_detail = models.HomeworkDetail.objects.filter(homework=homework, student=student).first()
        self.assertEqual(homework_detail.homework.title, '完成XX配置')

        study_record = models.StudyRecord.objects.get(course_lesson=course_lesson, student=student)
        self.assertEqual(study_record.status, 1)

    def test_view_api_no_authentication(self):
        """前后端分离部分里不需要做登录认证的视图"""
        category = self.client.get('/api/v1/category')
        self.assertEqual(category.status_code, 200)

        course = self.client.get('/api/v1/course')
        self.assertEqual(course.status_code, 200)

        degree = self.client.get('/api/v1/degree')
        self.assertEqual(degree.status_code, 200)

        degree = self.client.get('/api/v1/degree')
        self.assertEqual(degree.status_code, 200)

        detail = self.client.get('/api/v1/detail/1')
        self.assertEqual(detail.status_code, 200)

        chapter = self.client.get('/api/v1/chapter/1')
        self.assertEqual(chapter.status_code, 200)

        comment = self.client.get('/api/v1/comment/1')
        self.assertIsInstance(comment, models.Comment)
        # self.assertEqual(comment.status_code, 200)

        common_question = self.client.get('/api/v1/commonquestion/1')
        self.assertIsInstance(common_question, models.CommonQuestion)
        # self.assertEqual(commonquestion.status_code, 200)

        article = self.client.get('/api/v1/article')
        self.assertEqual(article.status_code, 200)

        register = self.client.post('api/v1/auth/register',
                                    data={'username': '王鸥', 'passwd': 123456, 'email': '15131651@qq.com'})
        self.assertEqual(register.status_code, 200)

    def test_backend_view(self):
        """测试后台登录部分"""
        login = self.client.post('/backend/login', data={'username': '刘文', 'password': 123456})
        self.assertEqual(login.status_code, 200)

        logout = self.client.get('/backend/logout')
        self.assertEqual(logout.status_code, 200)
