from startX.serivce.v1 import StartXHandler, get_m2m_display,Option
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe


class CourseDetailHandler(StartXHandler):
    def display_outline(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '课程大纲'
        record_url = reverse('startX:generic_courseoutline_list', kwargs={'course_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">课程大纲</a>' % record_url)

    def display_chapter(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '课程章节'
        record_url = reverse('startX:generic_coursechapter_list', kwargs={'course_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">课程章节</a>' % record_url)

    def display_coupon(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '课程优惠券'
        record_url = reverse('startX:generic_coupon_list', kwargs={'course_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">课程优惠券</a>' % record_url)

    def display_price_policy(self, model=None, is_header=None, *args, **kwargs):
        if is_header:
            return '价格策略'
        record_url = reverse('startX:generic_pricepolicy_list', kwargs={'course_id': model.pk})
        return mark_safe('<a target="_blank" href="%s">价格策略</a>' % record_url)

    list_display = ['course', 'brief', get_m2m_display('课程', 'teacher'), display_outline, display_chapter,
                    display_coupon, display_price_policy]

    # 常见问题

    search_list = ['course__contains']
    search_group = [
        Option('course'),
        Option('teacher'),
    ]