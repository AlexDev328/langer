from django.db import transaction
from rest_framework import serializers

from userprofile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'default_language')
