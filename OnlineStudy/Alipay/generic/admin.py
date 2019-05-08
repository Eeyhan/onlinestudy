from django.contrib import admin

# Register your models here.
from generic import models

admin.site.register(models.Account)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.CommonQuestion)
admin.site.register(models.Coupon)
admin.site.register(models.CouponDetail)
admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.Teacher)
admin.site.register(models.Order)
admin.site.register(models.OrderDetail)
admin.site.register(models.Degree)
admin.site.register(models.CourseChapter)
admin.site.register(models.CourseLesson)
admin.site.register(models.CourseOutline)
admin.site.register(models.TradeRecord)
admin.site.register(models.PricePolicy)

