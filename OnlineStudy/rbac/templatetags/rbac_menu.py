#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from rbac.service import urls

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    控制左侧菜单，根据当前登录用户所属权限来显示菜单
    :param request: request参数
    :return:
    """

    menu_dict = request.session[settings.INIT_MENU]

    # 对字典的key进行排序
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]  # 拿到菜单key对应的值
        val['class'] = 'hide'  # 给值设定一个class属性
        for per in val['children']:
            # 为当前被访问的链接添加一个active属性,默认选中特性
            # request.current_menu_selected一定会是一个可作为菜单的id
            if per['id'] == request.current_menu_selected:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {'menu_dict': ordered_dict}


@register.inclusion_tag('rbac/navigation.html')
def url_navigation(request):
    """
    控制路径导航
    :param request: request参数
    :return:
    """
    return {'navigation': request.url_navigation}


@register.filter
def has_permission_button(request, name):
    """
    粒度按钮控制，判断是否存在此权限
    :param request: request参数
    :param name: url别名
    :return:
    """
    if name in request.session[settings.INIT_PERMISSION]:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    '''
    生成带有原搜索条件的url
    :param request:
    :param name:
    :return:
    '''

    return urls.memory_url(request, name, *args, **kwargs)
