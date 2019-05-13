from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase, APIClient
from generic import models


class TestAPI(APITestCase):
    client_class = APIClient
    login = None

    def setUp(self):
        account_obj = models.Account.objects.create(brief='test', education=1, username='菲菲', passwd=123456,
                                                    email='10144894900@qq.com')

        self._login()

    def _login(self):
        login = self.client.post('/api/v1/auth/login', data={'username': '菲菲', 'passwd': 123456})

        self.assertEqual(login.status_code, 200)

    def test_rest_view(self):
        """前后端分离需要测试的视图"""

        """
        由于前后端分离，在用户登录做了token验证，目前没有好的解决方法解决单元测试携带token的方法来解决，大体的测试是没问题的
        """

        shopping = self.client.post('/api/v1/shopping', data={'course': 1, 'price_policy': 1, 'price': 20})

        self.assertEqual(shopping.status_code, 200)

        get_shopping = self.client.get('/api/v1/shopping', )
        self.assertEqual(get_shopping.status_code, 200)

        settlement = self.client.post('/api/v1/settlement',
                                      data={'course_list': 1})
        self.assertEqual(settlement.status_code, 200)

        get_settlement = self.client.get('/api/v1/settlement')
        self.assertEqual(get_settlement.status_code, 200)

        payment = self.client.post('/api/v1/payment',
                                   data={'balance': 0, 'price': 20, })
        self.assertEqual(payment.status_code, 200)

        get_payment = self.client.get('/api/v1/payment')
        self.assertEqual(get_payment.status_code, 200)

        coupon = self.client.post('/api/v1/coupon', data={'coupon': 1})
        self.assertEqual(coupon.status_code, 200)

        get_coupon = self.client.get('/api/v1/coupon', )
        self.assertEqual(get_coupon.status_code, 200)

        usercoupon = self.client.get('/api/v1/usercoupon')
        self.assertEqual(usercoupon.status_code, 200)

        usercourse = self.client.get('/api/v1/usercourse',
                                     data={'coupon': 1, })
        self.assertEqual(usercourse.status_code, 200)

        question = self.client.post('/api/v1/question',
                                    data={'question': '111151656asdf', })
        self.assertEqual(question.status_code, 200)

        get_question = self.client.get('/api/v1/question')
        self.assertEqual(get_question.status_code, 200)

        homework = self.client.post('/api/v1/homework', data={'homework': '11115asfwaefw1656asdf',
                                                              })
        self.assertEqual(homework.status_code, 200)

        get_homework = self.client.get('/api/v1/homework')
        self.assertEqual(get_homework.status_code, 200)
