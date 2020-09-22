from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, AuthorSerializer, StoryFeedSerializer, StoryViewerSerializer,StorySerializer
from rest_framework import permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from core.models import Post, Comment, Story
from .permissions import IsOwnerOrPostOwnerOrReadOnly, IsOwnerOrReadOnly
from rest_framework.response import Response
from core.pagination import FollowersLikersPagination, StoryViewerPagination


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeView(APIView):
    def get(self, request, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, post_id=None):
        post = Post.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsOwnerOrPostOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class LikersView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.get(
            pk=post_id).likes.all()
        return queryset


class ListFeedView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        queryset = Post.objects.all().filter(author__in=following_users)
        return queryset


class StoryViewSet(ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Story.objects.all().filter(author=self.request.user)


class GetStoryViewers(generics.ListAPIView):
    serializer_class = StoryViewerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StoryViewerPagination

    def get_queryset(self):
        story_id = self.kwargs['story_id']
        story_obj = Story.objects.get(pk=story_id)
        queryset = story_obj.views.all()
        return queryset


class GetStoryTagged(generics.ListAPIView):
    serializer_class = StoryViewerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StoryViewerPagination

    def get_queryset(self):
        story_id = self.kwargs['story_id']
        story_obj = Story.objects.get(pk=story_id)
        queryset = story_obj.tagged.all()
        return queryset


class GetFeedStories(generics.ListAPIView):
    serializer_class = StoryFeedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        queryset = Story.objects.all().filter(author__in=following_users)
        return queryset
