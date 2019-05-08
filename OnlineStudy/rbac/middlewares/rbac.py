#! /usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        current_url = request.path_info

        # 白名单，不需要做权限验证的url
        for valid in settings.VALID_URL:
            if re.match(valid, current_url):
                return None  # 中间件返回空，中间件不拦截，执行视图函数

        # 获取权限
        permission_dict = request.session.get(settings.INIT_PERMISSION)
        if not permission_dict:
            return HttpResponse('未获取到用户数据，请登录！')

        # 路径导航
        url_navigation = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处代码进行判断：/logout  /index

        for url in settings.NO_PERMISSION_LIST:
            if re.match(url,request.path_info):
                # 需要登录，但无需权限检验
                request.current_menu_selected = 0
                request.url_navigation = url_navigation
                return None

        flag = False
        for item in permission_dict.values():
            reg = '^%s$' % item['url']
            if re.match(reg, current_url):

                # 获取当前选中的菜单id ,先检测pid再检测id
                # 非菜单选项挂靠：如果是pid那么则是非菜单权限，通过此pid找到父级的id，如果是id则是二级菜单权限
                # 注意，此处的item['pid'] or item['id']，可能会有先后顺序
                request.current_menu_selected = item['pid'] or item['id']
                flag = True

                # 构建导航
                if item['pid']:
                    url_navigation.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                else:
                    url_navigation.extend([
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.url_navigation = url_navigation
                break

        if not flag:
            return HttpResponse('无权访问')
