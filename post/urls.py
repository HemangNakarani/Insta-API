from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include
from post import views
from .views import LikeView, AddCommentView, ManageCommentView, LikersView, ListFeedView, GetStoryViewers, \
    GetStoryTagged,GetFeedStories

app_name = 'post'

router = DefaultRouter()
router.register('manage', views.PostViewSet)
router.register('story/manage', views.StoryViewSet, 'Story')

urlpatterns = [
    path('', include(router.urls)),
    path('like/<uuid:post_id>/', LikeView.as_view(), name='like'),
    path('comment/<uuid:post_id>/', AddCommentView.as_view(), name='comment'),
    path('comment/<int:comment_id>/', ManageCommentView.as_view(), name='manage-comment'),
    path('likers/<uuid:post_id>/', LikersView.as_view(), name='get-likers'),
    path('feed/', ListFeedView.as_view(), name='feed'),
    path('story/viewers/<uuid:story_id>/', GetStoryViewers.as_view(), name='story-viewers'),
    path('story/tagged/<uuid:story_id>/', GetStoryTagged.as_view(), name='story-tagged'),
    path('story/', GetFeedStories.as_view(), name='story-feed'),
]
