from startX.serivce.v1 import StartXHandler, Option, get_field_display, get_datetime_format
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe
from generic import models
from django.utils.timezone import now


class PaymentRecordHandler(StartXHandler):
    def get_add_btn(self, request, *args, **kwargs):
        return None

    order_by = ['-id']
    list_display = [StartXHandler.display_checkbox,
                    'account', 'paid_fee', 'course',
                    get_field_display('交易类型', 'pay_type'),
                    get_field_display('申请状态', 'confirm_status'),
                    get_datetime_format('申请日期', 'apply_date'),
                    get_datetime_format('确认日期', 'confirm_date'),
                    'confirm_user', 'note']

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<account_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<account_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        account_id = kwargs.get('account_id')
        tpl = '<a href="%s">编辑</a>' % self.reverse_change_url(pk=model.pk, account_id=account_id)
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
        account_id = kwargs.get('account_id')
        return self.model_class.objects.filter(account_id=account_id)

    def action_multi_check(self, request, *args, **kwargs):
        """
        批量审批学生状态，审核确认入学
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 修改状态即可
        for pk in pk_list:
            payment_obj = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payment_obj:
                continue
            payment_obj.confirm_status = 2
            payment_obj.confirm_date = now()

            # 审批人

            payment_obj.save()

            payment_obj.account.level = 2
            payment_obj.account.save()

            payment_obj.account.student.student_status = 2
            payment_obj.account.student.save()

    action_multi_check.text = "批量确认入学"

    def action_multi_cancel(self, request, *args, **kwargs):
        """
        批量审批学生状态，审核驳回
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 修改状态即可
        for pk in pk_list:
            payment_obj = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payment_obj:
                continue
            payment_obj.confirm_status = 3
            payment_obj.save()

    action_multi_cancel.text = "批量驳回申请"

    def action_multi_drop_out(self, request, *args, **kwargs):
        """
        批量审批学生状态，审核退学
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 修改状态即可
        for pk in pk_list:
            payment_obj = self.model_class.objects.filter(id=pk, confirm_status=2).first()
            if not payment_obj:
                continue

            payment_obj.account.level = 3
            payment_obj.account.save()

            payment_obj.account.student.student_status = 4
            payment_obj.account.student.save()

    action_multi_drop_out.text = "批量退学"

    def action_multi_graduation(self, request, *args, **kwargs):
        """
        批量审批学生状态，审核确认毕业
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 修改状态即可
        for pk in pk_list:
            payment_obj = self.model_class.objects.filter(id=pk, confirm_status=2).first()
            if not payment_obj:
                continue

            payment_obj.account.student.student_status = 3
            payment_obj.account.student.save()

    action_multi_graduation.text = "批量毕业"

    action_list = [action_multi_check, action_multi_cancel, action_multi_drop_out, action_multi_graduation]
