from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.serializers import RegisterUserSerializer, ManageUserSerializer, FollowSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .permissions import ViewAccessPermission
from django.shortcuts import Http404
from core.pagination import FollowersLikersPagination


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"Message": "hello bro !!"}
        return Response(content)


class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = ManageUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            data = serializer.save()
            return Response({"message": "Updated successfully", "details": {
                "username": data.username,
                "email": data.email,
                "fullname": data.fullname,
                "bio": data.bio,
                "url": data.url,
                "profile_pic": str(data.profile_pic),
            }})

        else:
            return Response({"message": "Failed", "details": serializer.errors})


class UserProfileView(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (ViewAccessPermission,)

    def get_queryset(self):
        username = self.kwargs['username']
        try:
            obj = get_user_model().objects.get(username=username)
        except:
            raise Http404("No MyModel matches the given query.")

        self.check_object_permissions(self.request, obj)

        queryset = obj.followers.all()
        return queryset


class GetFollowingsView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (ViewAccessPermission,)

    def get_queryset(self):
        username = self.kwargs['username']
        try:
            obj = get_user_model().objects.get(username=username)
        except:
            raise Http404("No MyModel matches the given query.")

        self.check_object_permissions(self.request, obj)

        queryset = obj.following.all()
        return queryset


class RequestsView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowersLikersPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.requests.all()


class FollowUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user.is_authenticated:
            if from_user != to_user:
                if from_user in to_user.followers.all():
                    follow = False
                    from_user.following.remove(to_user)
                    to_user.followers.remove(from_user)
                elif from_user in to_user.requests.all():
                    follow = 'Already Requsted'
                else:
                    follow = 'Requsted'
                    to_user.requests.add(from_user)
        data = {
            'follow': follow
        }
        return Response(data)


class RequestProcessView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, username=None):
        opposite_user = get_user_model().objects.get(username=username)
        self_user = self.request.user
        resp = self.request.query_params.get('r')
        status = None
        if self_user.is_authenticated:
            if resp is not None:
                if opposite_user in self_user.requests.all():
                    if resp == 'Accept':
                        self_user.requests.remove(opposite_user)
                        self_user.followers.add(opposite_user)
                        opposite_user.following.add(self_user)
                        status = 'TrueAccepted'
                    else:
                        self_user.requests.remove(opposite_user)
                        status = 'TrueRejected'
                else:
                    status = 'User Has Not Requested'
            else:
                status = 'Add Accept or Reject as Query Params'
        data = {
            'status': status
        }
        return Response(data)
