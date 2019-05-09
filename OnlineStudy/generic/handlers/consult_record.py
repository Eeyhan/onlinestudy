from startX.serivce.v1 import StartXHandler, StartXModelForm, get_datetime_format
from django.urls import re_path
from django.utils.safestring import mark_safe
from generic import models
from django.shortcuts import HttpResponse
from .base_promission import PermissionHandler


class ConsultRecordModelForm(StartXModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['consultant', 'student']


class ConsultRecordHandler(PermissionHandler, StartXHandler):
    model_form_class = ConsultRecordModelForm
    order_by = ['-date', 'id']
    list_display = ['student', 'consultant', 'note',
                    get_datetime_format('跟进日期', 'date')]

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<student_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<student_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<student_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def save(self, request, form, is_update, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student_obj = models.Student.objects.filter(id=student_id).first()
        if not student_obj:
            return HttpResponse('非法操作')
        tutor = student_obj.tutor
        if not is_update:
            form.instance.student = student_obj.account
            form.instance.consultant = tutor
        form.save()

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

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        student_id = kwargs.get('student_id')
        tpl = '<a href="%s">编辑</a>' % self.reverse_change_url(pk=model.pk, student_id=student_id)
        return mark_safe(tpl)
