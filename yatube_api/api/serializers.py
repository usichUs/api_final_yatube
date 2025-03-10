from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Follow, User, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)  # Делаем post неизменяемым

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')  # Гарантируем, что они неизменяемые


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    validators = [UniqueTogetherValidator(
        queryset=Follow.objects.all(),
        fields=['user', 'following']
    )]

    def validate(self, data):
        if self.context['request'].user == data['following']:  # Запрещаем подписку на себя
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data

    class Meta:
        model = Follow
        fields = '__all__'  # Убраны лишние скобки


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  # Убраны лишние скобки
