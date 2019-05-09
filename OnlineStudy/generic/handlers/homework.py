from startX.serivce.v1 import StartXHandler, get_m2m_display
from django.urls import reverse
from django.utils.safestring import mark_safe
from .base_promission import PermissionHandler


class HomeworkHandler(PermissionHandler, StartXHandler):

    def display_outline(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '作业详情'
        record_url = reverse('startX:generic_homeworkdetail_list', kwargs={'homework_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">作业详情</a>' % record_url)

    list_display = [get_m2m_display('课程', 'courses'), 'title', get_m2m_display('章节', 'chapter'), 'content',
                    display_outline]

    search_list = ['courses__contains']
