from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, Option
from generic import models
from startX.forms.widgets import DateTimePickerInput
from .base_promission import PermissionHandler


class CourseModelForm(StartXModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'
        widgets = {
            'release_date': DateTimePickerInput,
        }


class CourseHandler(PermissionHandler, StartXHandler):
    model_form_class = CourseModelForm

    list_display = ['title', get_field_display('课程状态', 'status'),
                    get_field_display('课程难度', 'difficult'),
                    get_field_display('付费类型', 'course_type'), 'release_date', 'category',
                    'degree_course']

    # 常见问题

    search_list = ['title__contains']
    search_group = [
        Option('category'),
        Option('degree_course'),

    ]
