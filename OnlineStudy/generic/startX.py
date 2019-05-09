from startX.serivce.v1 import site
from generic import models
from generic.handlers.account import AccountHandler
from generic.handlers.course import CourseHandler
from generic.handlers.course_detail import CourseDetailHandler
from generic.handlers.course_outline import CourseOutlineHandler
from generic.handlers.course_chapter import CourseChapterHandler
from generic.handlers.course_coupon import CourseCouponHandler
from generic.handlers.course_price import CoursePriceHandler
from generic.handlers.course_lesson import CourseLessonHandler
from generic.handlers.order import OrderHandler
from generic.handlers.ordertail import OrderDetailHandler
from generic.handlers.payment_record import PaymentRecordHandler
from generic.handlers.student import StudentHandler
from generic.handlers.tutor import TutorHandler
from generic.handlers.consult_record import ConsultRecordHandler
from generic.handlers.article import ArticleHandler
from generic.handlers.homework import HomeworkHandler
from generic.handlers.question import QuestionHandler
from generic.handlers.homework_detail import HomeworkDetailHandler
from generic.handlers.study_record import StudyRecordHandler
from generic.handlers.register_trend import AccountRegisterTrendHandler
from generic.handlers.order_trend import OrderTrendHandler

site.register(models.Account, AccountHandler)
site.register(models.Account, AccountRegisterTrendHandler, prev='trend')
site.register(models.Course, CourseHandler)
site.register(models.CourseDetail, CourseDetailHandler)
site.register(models.CourseOutline, CourseOutlineHandler)
site.register(models.CourseChapter, CourseChapterHandler)
site.register(models.Coupon, CourseCouponHandler)
site.register(models.PricePolicy, CoursePriceHandler)
site.register(models.CourseLesson, CourseLessonHandler)
site.register(models.Order, OrderHandler)
site.register(models.Order, OrderTrendHandler,prev='trend')
site.register(models.OrderDetail, OrderDetailHandler)
site.register(models.PaymentRecord, PaymentRecordHandler)
site.register(models.Student, StudentHandler)
site.register(models.Tutor, TutorHandler)
site.register(models.ConsultRecord, ConsultRecordHandler)
site.register(models.Article, ArticleHandler)
site.register(models.Homework, HomeworkHandler)
site.register(models.StudyQuestion, QuestionHandler)
site.register(models.HomeworkDetail, HomeworkDetailHandler)
site.register(models.StudyRecord, StudyRecordHandler)
