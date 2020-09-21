from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import Post, Comment
from django.core.paginator import Paginator
from rest_framework.settings import api_settings


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        depth = 1
        fields = ('id', 'email', 'fullname', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5},
                        'username': {'min_length': 3}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def to_representation(self, obj):
        token = Token.objects.create(user=obj)
        return {
            'id': obj.id,
            'username': obj.username,
            'email': obj.email,
            'token': token.key,
        }


class ManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password',
                  'fullname', 'bio', 'url', 'profile_pic')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5},
                        'username': {'min_length': 3}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for listing all followers"""

    class Meta:
        model = get_user_model()
        fields = ('username', 'profile_pic')


class UserPostsSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user profile"""
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'photo', 'text', 'location', 'number_of_likes',
                  'number_of_comments', 'posted_on')

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user posts"""
    number_of_posts = serializers.SerializerMethodField()
    followed_by_req_user = serializers.SerializerMethodField()
    user_posts = serializers.SerializerMethodField('paginated_user_posts')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'fullname',
                  'bio', 'url', 'profile_pic', 'number_of_followers',
                  'number_of_following', 'number_of_posts', 'followed_by_req_user', 'user_posts')

    def get_number_of_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def paginated_user_posts(self, obj):
        if self.get_followed_by_req_user(obj):
            page_size = 3
            paginator = Paginator(obj.user_posts.all(), page_size)
            page = self.context['request'].query_params.get('page') or 1

            user_posts = paginator.page(page)
            serializer = UserPostsSerializer(user_posts, many=True)

            return serializer.data
        else:
            return [{'Locked': 'Follow the User to See their Posts'}]

    def get_followed_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.followers.all()
