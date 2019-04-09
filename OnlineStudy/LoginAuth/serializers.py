from rest_framework import serializers
from generic.models import Account
import hashlib


class RegisterSerializer(serializers.ModelSerializer):
    """注册"""
    education = serializers.CharField(source='get_education_display')

    class Meta:
        model = Account
        fields = ['id', 'username', 'passwd', 'brief', 'education', 'career', 'balance']

    def create(self, validated_data):
        # {"username":"海丰","passwd":"1234","career":"test","brief":"test","education":1}
        print(validated_data)
        username = validated_data['username']
        passwd = validated_data['passwd']
        education = validated_data['get_education_display']
        brief = validated_data['brief']
        career = validated_data['career']
        hash_key = 'password'
        passwd = passwd + hash_key
        passwd_md5 = hashlib.md5(passwd.encode()).hexdigest()
        user_obj = Account.objects.create(username=username, passwd=passwd_md5,
                                          education=education, brief=brief,
                                          career=career)
        return user_obj
