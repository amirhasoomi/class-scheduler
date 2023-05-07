from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile, User
from .serializers import (RegisterSerializer, LoginSerializer,
                          ChangePasswordSerializer, ProfileSerializer,
                          UserSerializer)
from utils.permissions import IsAdmin
from .apps import AuthenticationConfig as Conf


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class ChangePasswordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        return self.request.user.profile


class UsertypeView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MembersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(user__user_type=Conf.USER_TYPE_MEMBER)


class JudgesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(user__user_type=Conf.USER_TYPE_JUDGE)


class AllUsersView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
