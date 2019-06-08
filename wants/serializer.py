# coding: utf-8

from rest_framework import serializers

from .models import User, Want, Like


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'twitter_url', 'intro_text', 'image', 'is_active', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            is_active=validated_data['is_active'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class WantSerializer(serializers.ModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = Want
        # fields = ('id', 'user', 'content', 'status', 'target_date', 'publish_set', 'achieve_date', 'achieve_text', 'achieve_url', 'like_num', 'create_date')
        fields = ('id', 'user', 'content', 'status', 'target_date', 'publish_set', 'achieve_date', 'achieve_text', 'achieve_url', 'like_num', 'display_order', 'create_date')


    # def __init__(self, *args, **kwargs):
    #     self._user = kwargs.pop('user')
    #     super(WantSerializer, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     want = super(WantSerializer, self).save(commit=False)
    #     want.user = self._user
    #     if commit:
    #         want.save()
    #     return want

    # def create(self, request, validated_data):
    #     print(request.user.id)
    #     print('kitazo')
    #     want = Want(
    #         content = validated_data['content'],
    #         status = validated_data['status'],
    #         publish_set = validated_data['publish_set'],
    #         user = request.user.id
    #     )
    #     print(want)
    #     want.save()
    #     return want


class LikeSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # want = WantSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user', 'want')


