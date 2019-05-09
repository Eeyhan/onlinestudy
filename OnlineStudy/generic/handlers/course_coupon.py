from startX.serivce.v1 import StartXHandler
from django.urls import re_path
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class CourseCouponHandler(PermissionHandler, StartXHandler):

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<course_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<course_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<course_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<course_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_del_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit_del(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        course_id = kwargs.get('course_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=model.pk, course_id=course_id),
            self.reverse_delete_url(pk=model.pk, course_id=course_id))
        return mark_safe(tpl)

    def get_model_queryset(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        return self.model_class.objects.filter(object_id=course_id)

    list_display = [
        # get_field_display('课程', 'content_object'),
        'title', 'coupon_type', 'count']
