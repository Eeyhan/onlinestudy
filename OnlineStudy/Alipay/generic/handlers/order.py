from startX.serivce.v1 import StartXHandler, get_field_display, get_datetime_format
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe


class OrderHandler(StartXHandler):
    order_by = ['-id']

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def display_orderdetail(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '订单详情'
        record_url = reverse('startX:generic_orderdetail_list', kwargs={'order_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">订单详情</a>' % record_url)

    def display_paymentrecord(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '缴费申请'
        record_url = reverse('startX:generic_paymentrecord_list', kwargs={'account_id': model.account_id})
        return mark_safe('<a target="_blank" href="%s">缴费申请</a>' % record_url)

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    list_display = [
        'account', 'payment_amount',
        get_field_display('交易类型', 'payment_type'),
        get_field_display('订单状态', 'status'),
        get_datetime_format('生成时间', 'date'),
        get_datetime_format('付款时间', 'pay_time'),
        'payment_number', 'order_nubmer', display_orderdetail, display_paymentrecord]

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value

    search_list = ['account__contains', ]
