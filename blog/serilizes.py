from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='blog:user-detail',
        lookup_field='pk'
    )
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='blog:post-detail',
        read_only=True,
        lookup_field='pk'
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'posts']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='blog:post-detail',
        lookup_field='pk'
    )

    owner = serializers.HyperlinkedRelatedField(
        view_name='blog:user-detail',
        read_only=True,
        lookup_field='pk'
    )


    class Meta:
        model = Post
        fields = ['url', 'title', 'content', 'owner']