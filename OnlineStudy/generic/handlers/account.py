from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm
from generic import models
from .base_promission import PermissionHandler


class AccountModelForm(StartXModelForm):
    class Meta:
        model = models.Account
        fields = ['id', 'username', 'email', 'level']


class AccountHandler(PermissionHandler, StartXHandler):
    order_by = ['level', 'id']
    model_form_class = AccountModelForm
    list_display = ['username', 'email', 'brief', get_field_display('学历', 'education'), 'career',
                    get_field_display('用户等级', 'level')]
    search_list = ['username__contains']
