from collections import OrderedDict
from django.utils.module_loading import import_string
from django.conf import settings
from django.urls.resolvers import URLResolver, URLPattern
import re


def check_url_exclude(url):
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursive_url(pre_namespace, pre_url, urlpattern, url_order_dict):
    """
    递归发现url
    :param pre_namespace: 根别名
    :param pre_url: url前缀
    :param urlpattern: 路由关系表
    :param url_order_dict  有序url字典,用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpattern:
        if isinstance(item, URLPattern):  # 非路由分发
            if not item.name:
                continue
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + item.pattern.regex.pattern
            url = url.replace('^', '').replace('$', '')  # 去掉正则表达式里的前缀和后缀
            if check_url_exclude(url):
                continue
            url_order_dict[name] = {'name': name, 'url': url}
        elif isinstance(item, URLResolver):  # 路由分发
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    # namespace = item.namespace  # 另一种写法
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None

            # print(item.pattern.regex.pattern)
            recursive_url(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_order_dict)


def get_all_url_dict():
    url_order_dict = OrderedDict()
    root = import_string(settings.ROOT_URLCONF)
    recursive_url(None, '/', root.urlpatterns, url_order_dict)
    return url_order_dict
