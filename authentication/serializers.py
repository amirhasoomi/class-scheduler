from rest_framework import serializers
from .models import Profile, User
from django.contrib.auth.hashers import make_password
from .apps import AuthenticationConfig as Conf


class RegisterSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        if Profile.objects.filter(mobile=attrs['mobile']).exists():
            raise serializers.ValidationError(
                dict(mobile=['mobile is used before!', ]))
        return attrs

    def create(self, validated_data):
        profile, _ = Profile.get_or_create(
            mobile=validated_data['mobile'],
            defaults=dict(password=make_password(validated_data['password']))
        )
        return {
            'pk': profile.pk,
            'mobile': profile.mobile,
            'user_type': profile.user.user_type,
        }


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    new_account = serializers.BooleanField(read_only=True)
    user_type = serializers.ChoiceField(
        choices=Conf.USER_TYPES, read_only=True)

    def validate(self, attrs):
        mobile = attrs['mobile']
        if not Profile.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError(
                dict(mobile=['Account is not registerd!', ]))
        instance = Profile.objects.get(mobile=mobile)
        if not instance.verify_password(attrs['password']):
            raise serializers.ValidationError(
                dict(password=['Invalid Password', ]))
        attrs['mobile'] = mobile
        return attrs

    def create(self, validated_data):
        profile = Profile.objects.get(mobile=validated_data['mobile'])
        refresh, access = profile.user.api_token()

        return {
            'access': access,
            'refresh': refresh,
            'user_type': profile.user.user_type,
        }


class ChangePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    result = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = attrs['user']
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        instance = Profile.objects.get(user=user)
        if not instance.verify_password(attrs['password']):
            raise serializers.ValidationError(
                dict(password=['Invalid Password.', ]))
        if instance.verify_password(attrs['new_password']):
            raise serializers.ValidationError(
                dict(
                    new_password=[
                        'naw password cant be same as current.', ]))
        if not new_password == confirm_password:
            raise serializers.ValidationError(
                dict(
                    confirm_password=[
                        'New Password and Confirm Password must be match.', ]))
        attrs['user'] = user
        attrs['new_password'] = new_password
        return attrs

    def create(self, validated_data):
        Profile.objects.filter(user=validated_data['user']).update(
            password=make_password(validated_data['new_password']))
        return {
            'result': "your password has been changed successfully.",
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'username', 'f_name', 'l_name',
                  'birthday', 'phone', 'mobile', 'email',
                  'address', 'ldc', 'major', 'orientation',
                  'Country', 'state', 'city', 'specialty', 'national_id')
        read_only_fields = ('user',)

    def validate(self, attrs):
        username = attrs['username'].lower()
        if Profile.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                dict(username=['username is used before!', ]))
        if Profile.objects.filter(mobile=attrs['mobile']).exists():
            raise serializers.ValidationError(
                dict(mobile=['mobile is used before!', ]))
        if Profile.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                dict(email=['email is used before!', ]))
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        read_only_fields = ('__all__',)
