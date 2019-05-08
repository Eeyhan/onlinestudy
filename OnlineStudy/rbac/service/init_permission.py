#! /usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf import settings


def init_permission(current_user, request):
    # 获取当前用户的权限，放入session中
    # 一个用户有多个角色，也就有多个权限，所以很有可能有重复;
    # 也有可能有角色新创建没有任何权限，所以需要过滤
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                      'permissions__title',
                                                                                      'permissions__url',
                                                                                      'permissions__name',
                                                                                      'permissions__pid',
                                                                                      'permissions__pid__title',
                                                                                      'permissions__pid__url',
                                                                                      'permissions__menu_id',
                                                                                      'permissions__menu__title',
                                                                                      'permissions__menu__icon').distinct()
    # QuerySet对象不能直接存放，因为做了dump

    # 构建权限
    permission_dict = {}

    # 菜单字典
    menu_dict = {}
    for item in permission_queryset:
        # 构建权限表
        permission_dict[item['permissions__name']] = (
            {
                'id': item['permissions__id'],
                'url': item['permissions__url'],
                'title':item['permissions__title'],
                'pid': item['permissions__pid'],
                'p_url':item['permissions__pid__url'],
                'p_title':item['permissions__pid__title']
            })

        # 构建菜单表
        menu_id = item['permissions__menu_id']

        # 数据库表里为空，不能为菜单的权限，跳过本次循环
        if not menu_id:
            continue

        node = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url']}

        # 最开始字典为空，菜单id不在菜单字典内，构建字典类型

        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }
        # 已构建字典类型，字典不为空，直接添加
        else:
            menu_dict[menu_id]['children'].append(node)

    # for k,v in permission_dict.items():
    #     print(k,'---',v)
    # print('menu_dict',menu_dict)
    request.session[settings.INIT_PERMISSION] = permission_dict
    request.session[settings.INIT_MENU] = menu_dict
