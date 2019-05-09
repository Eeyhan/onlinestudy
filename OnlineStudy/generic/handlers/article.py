from startX.serivce.v1 import StartXHandler, get_datetime_format, StartXModelForm
from generic import models
from .base_promission import PermissionHandler


class ArticleModelForm(StartXModelForm):
    class Meta:
        model = models.Article
        exclude = ['date']


class ArticleHandler(PermissionHandler, StartXHandler):
    model_form_class = ArticleModelForm
    order_by = ['date', '-id', ]
    list_display = ['title', 'content',
                    get_datetime_format('发布日期', 'date'), ]
    search_list = ['title__contains']
