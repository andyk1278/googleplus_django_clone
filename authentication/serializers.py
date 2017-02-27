from django.contrib.auth.models import User

from rest_framework import serializers
from authentication.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = (
        'id', 'username', 'email', 'first_name', 'last_name', 'password'
    )
    write_only_fields = ('password',)

def restore_object(self, attrs, instance=None):
    user = super(UserSerializer, self).restore_object(attrs, instance)

    password = attrs.get('password', None)

    if password:
        user.set_password(password)

    return user

class UserProfileSerializer(serializers.ModelSerializer)
    # Since UserProfile does not have an id attribute, an id field where the
    # source is UserProfile.pk is created to act as the id of the associated User instead.
    id = serializers.IntegerField(source='pk', read_only=True)

    # When serializing UserProfile, information of the User is desired to be included
    # since UserProfile is created to 'extend' the User.  username,email,first/last_name
    # are chosen, as shown below, and each fields 'source' attribute is set
    # equal to the value of <related model>.<related model attribute>
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'tagline',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def restore_object(self, attrs, instance=None):
        profile = super(UserProfileSerializer, self).restore_object(attrs, instance)

        if profile:
            user = profile.user

            user.email = attrs.get('user.email', user.email)
            user.first_name = attrs.get('first_name', user.first_name)
            user.last_name = attrs.get('last_name', user.last_name)

            # when updating a related model, it must also be explicitly saved
            user.save()

        return profile
