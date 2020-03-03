from rest_framework.serializers import ModelSerializer,SerializerMethodField, HyperlinkedIdentityField
from rest_framework import status
from ..models import NewsFeedPost

class NewsFeedPostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'insta-api:post_detail_api',
        lookup_field ='pk',
    )
    userProfileImage = SerializerMethodField()
    userName = SerializerMethodField()
    userProfileUrl = SerializerMethodField()
    comments = HyperlinkedIdentityField(
        view_name='comments-api:api_list_comments',
        lookup_field='pk',
    )
    likes = SerializerMethodField()
    timestamp = SerializerMethodField()
    updated = SerializerMethodField()
    image = SerializerMethodField()
    caption = SerializerMethodField()
    liked = SerializerMethodField()
    viewLikes = HyperlinkedIdentityField(
        view_name='insta-api:post_likes_api',
        lookup_field='pk'
    )
    class Meta:
        model = NewsFeedPost
        fields = [
            'url',
            'userProfileImage',
            'userName',
            'userProfileUrl',
            'image',
            'caption',
            'timestamp',
            'updated',
            'comments',
            'liked',
            'likes',
            'viewLikes'
        ]
    def get_image(self, obj):
        return obj.post.image.url
    def get_likes(self,obj):
        return obj.post.like_set.count()
    def get_userProfileImage(self,obj):
        return obj.post.user.account.get_image_url()
    def get_userName(self,obj):
        return str(obj.post.user.username)
    def get_userProfileUrl(self,obj):
        return obj.post.user.account.get_full_url()
    def get_timestamp(self,obj):
        return obj.post.timestamp
    def get_updated(self,obj):
        return obj.post.updated
    def get_caption(self, obj):
        return obj.post.caption
    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            liked = obj.post.like_set.get(user = user)
            if liked:
                return True
            else:
                return False
        else:
            return False