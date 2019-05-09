from startX.serivce.v1 import StartXHandler
from django.urls import re_path
from .base_promission import PermissionHandler


class TutorHandler(PermissionHandler, StartXHandler):

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^add/$', self.wrapper(self.add_view), name=self.get_add_name),
            re_path(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),
            re_path(r'^del/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_del_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

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
            value.append(type(self).display_edit_del)
        return value

    order_by = ['id']
    list_display = ['account']
