from startX.serivce.v1 import StartXHandler, get_m2m_display, get_field_display
from django.urls import re_path
from django.utils.safestring import mark_safe


class OrderDetailHandler(StartXHandler):

    def get_add_btn(self, request, *args, **kwargs):
        return

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<order_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<order_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        order_id = kwargs.get('order_id')
        tpl = '<a href="%s">编辑</a>' % self.reverse_change_url(pk=model.pk, order_id=order_id)
        return mark_safe(tpl)

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

    def get_model_queryset(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        return self.model_class.objects.filter(order_id=order_id)

    list_display = [
        'order', 'original_price', 'price', 'valid_period', get_field_display('交易类型', 'transaction_type'),
        'transaction_number', 'product']
