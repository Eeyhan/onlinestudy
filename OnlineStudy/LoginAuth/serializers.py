from rest_framework import serializers
from generic.models import Account
import hashlib


class RegisterSerializer(serializers.ModelSerializer):
    """注册"""
    CHOICES = ((0, '大专'), (1, '本科'), (2, '研究生'), (3, '博士'), (4, '硕士'), (5, '其他'))
    education = serializers.ChoiceField(choices=CHOICES, source='get_education_display',read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'passwd', 'brief', 'education', 'career', 'balance','email']

    def create(self, validated_data):
        """添加"""
        username = validated_data['username']
        passwd = validated_data['passwd']
        email = validated_data['email']
        hash_key = 'password'
        passwd = passwd + hash_key
        passwd_md5 = hashlib.md5(passwd.encode()).hexdigest()
        user_obj = Account.objects.create(username=username, passwd=passwd_md5, email=email)
        return user_obj

    def update(self, instance, validated_data):
        """修改"""

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.education = validated_data.get('education', instance.education)
        instance.brief = validated_data.get('brief', instance.brief)
        instance.career = validated_data.get('career', instance.career)
        instance.save()
        return instance
