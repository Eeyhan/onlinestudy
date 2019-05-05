from django.urls import path
from generic import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    path('course', views.CourseView.as_view()),
    path('degree', views.DegreeView.as_view()),
    path('detail/<int:pk>', views.CourseDetailView.as_view()),
    path('chapter/<int:pk>', views.CourseChapterView.as_view()),
    path('comment/<int:pk>', views.CourseCommentView.as_view()),
    path('commonquestion/<int:pk>', views.CourseCommonquestionView.as_view()),
    path('shopping', views.ShoppingView.as_view()),
    path('settlement', views.SettlementView.as_view()),
    path('payment', views.PaymentView.as_view()),
    path('coupon', views.CouponDistributionView.as_view()),
    path('usercoupon', views.UserCouponView.as_view()),
    path('usercourse', views.UserCourseView.as_view()),
    path('question', views.QuestionView.as_view()),
]
