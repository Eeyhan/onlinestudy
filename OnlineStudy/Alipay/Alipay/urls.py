from django.urls import path
from Alipay.views import AlipayView
from Alipay.views import PayHandlerView

urlpatterns = [
    path('pay/',AlipayView.as_view()),
    path('alipay_handler',PayHandlerView.as_view())
]