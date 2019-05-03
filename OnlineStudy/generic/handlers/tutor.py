from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_m2m_display
from generic import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class TutorHandler(StartXHandler):

    def display_outline(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '学员跟进记录'
        record_url = reverse('startX:generic_consultrecord_list', kwargs={'tutor_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">学员跟进记录</a>' % record_url)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        预留钩子函数
        :param form:
        :param is_update:是否是更新数据，true即为更新，false即为添加数据
        :return:
        """
        form.instance.account.level = 1
        form.instance.account.save()
        form.save()

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    order_by = ['id']
    list_display = ['account', ]
