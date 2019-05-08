from django.urls import re_path
from rbac.views import role, user, menu

urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name='role_add'),
    re_path(r'^role/edit/(?P<id>\d+)/$', role.role_edit, name='role_edit'),
    re_path(r'^role/del/(?P<id>\d+)/$', role.role_del, name='role_del'),

    # re_path(r'^user/list/$',user.user_list,name='user_list'),
    # re_path(r'^user/add/$',user.user_add,name='user_add'),
    # re_path(r'^user/edit/(?P<id>\d+)/$',user.user_edit,name='user_edit'),
    # re_path(r'^user/del/(?P<id>\d+)/$',user.user_del,name='user_del'),
    # re_path(r'^user/reset/password/(?P<id>\d+)/$',user.user_reset_password,name='user_reset_password'),

    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<id>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<id>\d+)/$', menu.menu_del, name='menu_del'),

    re_path(r'^secondmenu/add/(?P<pk>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    re_path(r'^secondmenu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'^secondmenu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),

    re_path(r'^permission/add/(?P<pk>\d+)/$', menu.permission_add, name='permission_add'),
    re_path(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),

    re_path(r'^multi/permission/$', menu.multi_permission, name='multi_permission'),
    re_path(r'^multi/permission/del/(?P<id>\d+)/$', menu.multi_permission_del, name='multi_permission_del'),
    re_path(r'^distribute/permission/$', menu.distribute_permission, name='distribute_permission'),

]
