from rest_framework import serializers
from generic import models


class CategorySerializer(serializers.ModelSerializer):
    """课程分类"""

    class Meta:
        model = models.Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """课程"""
    status = serializers.CharField(source='get_status_display')
    lesson = serializers.CharField(source='coursedetail.lesson')
    price = serializers.SerializerMethodField()
    price_policy = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    free_course = serializers.SerializerMethodField()

    """
    course_img本来可以直接获取，但是django配置了media文件夹+model表设置了ImageField字段
    在取图片时会自动添加[media/]路径 
    在真实部署时，注释掉这个部分       
    """
    course_img = serializers.SerializerMethodField()

    def get_price_policy(self, obj):
        """获取价格策略"""
        return obj.price_policy.all().order_by('price').first().id

    def get_course_img(self, obj):
        """获取课程图片"""
        return str(obj.course_img)

    def get_price(self, obj):
        """返回最低价"""
        return obj.price_policy.all().order_by('price').first().price

    def get_teacher(self, obj):
        """获取讲师"""
        res = obj.coursedetail.teacher.all()
        return [{"username": teacher.username, "title": teacher.title} for teacher in res]

    def get_free_course(self, obj):
        res = obj.course_chapters.all().first().course_lesson.all()
        return [{"title": lesson.title} for lesson in res if lesson.free_trail]

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'course_img', 'status', 'study_number', 'price',
                  'price_policy', 'lesson', 'teacher', 'free_course']


class CourseDetailSerializer(serializers.ModelSerializer):
    """课程详情"""
    title = serializers.CharField(source='course.title')
    course_img = serializers.CharField(source='course.course_img')
    study_number = serializers.CharField(source='course.study_number')
    difficult = serializers.CharField(source='course.get_difficult_display')
    course_id = serializers.IntegerField(source='course.id')
    teacher = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    course_outline = serializers.SerializerMethodField()
    recommend_course = serializers.SerializerMethodField()

    def get_recommend_course(self, obj):
        """推荐课程"""
        res = obj.recommend_course.all()
        if len(res):
            return [{'title': course.title, 'brief': course.coursedetail.brief, 'course_img': str(course.course_img)}
                    for course in
                    obj.recommend_course.all()]
        else:
            pass

    def get_teacher(self, obj):
        """讲师"""
        res = obj.teacher.all()
        return [{"title": teacher.title, "username": teacher.username, 'brief': teacher.brief,
                 'teacher_img': str(teacher.teacher_img)}
                for teacher in res]

    def get_prices(self, obj):
        """价格"""
        res = obj.course.price_policy.all().order_by('price')
        return [{"valid_period": price.get_valid_period_display(), 'price': price.price, 'id': price.id} for price in
                res]
        # return obj.course.price_policy.all().order_by('price')

    def get_course_outline(self, obj):
        """大纲"""
        res = obj.course_outline.all()
        return [{"content": courseOutline.content} for courseOutline in res]

    class Meta:
        model = models.CourseDetail
        fields = ['course_id', 'title', 'course_img', 'course_review', 'study_number', 'difficult', 'prices',
                  'lesson', 'teacher', 'brief', 'why_study', 'slogan', 'feature',
                  'point', 'course_outline', 'harvest', 'object_person', 'recommend_course',
                  'prerequisite']


class ChapterSerializer(serializers.ModelSerializer):
    """课程章节、全部课时"""
    chapter_lesson = serializers.SerializerMethodField()

    def get_chapter_lesson(self, obj):
        res = obj.course_lesson.all().order_by('order')
        return [{"id": cou_les.id, "title": cou_les.title, 'free_trail': cou_les.free_trail} for cou_les in res]

    class Meta:
        model = models.CourseChapter
        fields = ['id', 'title', 'chapter_lesson']


class CommentSerializer(serializers.ModelSerializer):
    """用户评论"""
    account = serializers.CharField(source='account.username')

    class Meta:
        model = models.Comment
        fields = ['id', 'account', 'comment_date', 'content']


class CommonQuestionSerializer(serializers.ModelSerializer):
    """常见问题"""

    class Meta:
        model = models.CommonQuestion
        fields = ['id', 'question', 'answer']
