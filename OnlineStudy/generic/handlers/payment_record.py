from startX.serivce.v1 import StartXHandler, Option, get_field_display, get_datetime_format
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe
from generic import models


class PaymentRecordHandler(StartXHandler):
    def get_add_btn(self, request, *args, **kwargs):
        return None

    order_by = ['-id']
    list_display = [StartXHandler.display_checkbox,
                    'account', 'paid_fee', 'course',
                    get_field_display('交易类型', 'pay_type'),
                    get_field_display('申请状态', 'confirm_status'),
                    get_datetime_format('申请日期', 'date'),
                    get_datetime_format('确认日期', 'confirm_date'), 'confirm_user', 'note']

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<account_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<account_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_model_queryset(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        return self.model_class.objects.filter(customer_id=account_id)

    def action_multi_check(self, request, *args, **kwargs):
        """
        批量审批
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 做验证，数据库是否确有选中的用户
        for pk in pk_list:
            account_obj = models.Account.objects.filter(id=pk).first()
            student_obj = models.Student.objects.filter(id=pk).first()
            if not (account_obj and student_obj):
                continue

            # 将该用户的类型改成学员，该用户的相关添加到student表里
            account_obj.level = 2
            account_obj.save()
            student_obj.student_status = 2
            student_obj.save()

    action_multi_check.text = '批量审批'
    action_list = [action_multi_check, ]
