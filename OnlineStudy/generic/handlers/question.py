from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_datetime_format
from generic import models
from django.urls import re_path
from startX.forms.widgets import DateTimePickerInput


class QuestionModelForm(StartXModelForm):
    class Meta:
        model = models.StudyQuestion
        fields = ['answer', 'answer_date']
        widgets = {
            'answer_date': DateTimePickerInput,
        }


class QuestionHandler(StartXHandler):
    model_form_class = QuestionModelForm

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),
            re_path(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    list_display = ['student',
                    'question',
                    get_datetime_format('提问时间', 'question_date'),
                    'tutor',
                    'answer',
                    get_datetime_format('回答时间', 'answer_date')
                    ]

    search_list = ['title__contains']

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
        user_id = request.session['userinfo']['id']
        return self.model_class.objects.filter(tutor__account_id=user_id)
