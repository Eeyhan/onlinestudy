from startX.serivce.v1 import StartXHandler, StartXModelForm, get_field_display, Option
from django.urls import re_path
from django.utils.safestring import mark_safe
from generic import models
from .base_promission import PermissionHandler


class CourseLessonModelForm(StartXModelForm):
    class Meta:
        model = models.CourseLesson
        fields = '__all__'


class CourseLessonHandler(PermissionHandler, StartXHandler):

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<course_chapter_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/(?P<course_chapter_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<course_chapter_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<course_chapter_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
                    name=self.get_del_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit_del(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        course_chapter_id = kwargs.get('course_chapter_id')
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=model.pk, course_chapter_id=course_chapter_id),
            self.reverse_delete_url(pk=model.pk, course_chapter_id=course_chapter_id))
        return mark_safe(tpl)

    def get_model_queryset(self, request, *args, **kwargs):
        course_chapter_id = kwargs.get('course_chapter_id')
        return self.model_class.objects.filter(chapter_id=course_chapter_id)

    list_display = [
        'title', 'order', get_field_display('课程顺序', 'course_lesson_type'), 'free_trail', 'lesson_link']

    search_list = ['title__contains']
