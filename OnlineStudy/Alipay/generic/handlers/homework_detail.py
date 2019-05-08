from startX.serivce.v1 import StartXHandler, get_m2m_display, StartXModelForm
from django.urls import re_path, reverse
from django.utils.safestring import mark_safe
from generic import models
from django.conf import settings
from django.shortcuts import HttpResponse


class HomeworkDetailModelForm(StartXModelForm):
    class Meta:
        model = models.HomeworkDetail
        fields = ['status', 'critic']


class HomeworkDetailHandler(StartXHandler):
    model_form_class = HomeworkDetailModelForm

    def get_add_btn(self, request, *args, **kwargs):
        return

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/(?P<homework_id>\d+)/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<homework_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^download/(?P<pk>\d+)/$', self.wrapper(self.download),
                    name=self.get_url_name('download')),
        ]
        patterns.extend(self.extra_url())
        return patterns

    def display_edit(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        homework_id = kwargs.get('homework_id')
        tpl = '<a href="%s">编辑</a>' % self.reverse_change_url(pk=model.pk, homework_id=homework_id)
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
        homework_id = kwargs.get('homework_id')
        user_id = request.session['userinfo']['id']
        user_obj = models.Tutor.objects.filter(account_id=user_id).first()
        # 登录的导师只能看自己所对应的所有学员作业情况
        return self.model_class.objects.filter(homework_id=homework_id, teacher=user_obj)

    def display_download(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '作业文件'
        name = "%s:%s" % (self.site.namespace, self.get_url_name('download'),)
        reverse_url = reverse(name, kwargs={'pk': model.pk})
        return mark_safe('<a target="_blank" href="%s">下载作业</a>' % reverse_url)

    def download(self, request, pk, *args, **kwargs):
        """
        下载学员的作业
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        file = str(self.model_class.objects.filter(id=pk).first().file)
        file_link = settings.BASE_FILE + file
        return HttpResponse('<a href="%s" download="%s">点我下载</a>' % (file_link, file))

    list_display = [
        'homework', get_m2m_display('学生', 'student'), 'status', display_download, 'critic']
    search_list = ['student__contains']
