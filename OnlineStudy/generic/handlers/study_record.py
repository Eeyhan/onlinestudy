from startX.serivce.v1 import StartXHandler, get_m2m_display, get_field_display
from django.urls import re_path
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class StudyRecordHandler(PermissionHandler, StartXHandler):

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

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        student_id = kwargs.get('student_id')
        tpl = '<a href="%s">编辑</a> ' % self.reverse_change_url(pk=model.pk, student_id=student_id)
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

    list_display = [
        get_m2m_display('课时', 'course_lesson'), get_m2m_display('学生', 'student'), get_field_display('状态', 'status'), ]
