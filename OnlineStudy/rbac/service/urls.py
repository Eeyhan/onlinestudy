from django.urls import reverse
from django.http import QueryDict


def memory_reverse(request, url_name, *args, **kwargs):
    '''
    反向生成url
    :param request: request参数
    :param url_name: url别名
    :param args: 参数
    :param kwargs: 参数
    :return: 返回一个带有参数的真实url
    '''

    url = reverse(url_name, args=args, kwargs=kwargs)
    query = request.GET.get('_filter')
    if query:
        url = '%s?%s' % (url, query,)
    print('url',url)
    return url


def memory_url(request, name, *args, **kwargs):
    '''
    生成带有原搜索条件的url
    :param request:
    :param name:
    :return:
    '''

    base_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return base_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return '%s?%s' % (base_url, query_dict.urlencode())
