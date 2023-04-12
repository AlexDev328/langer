from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from userprofile.api.serializers import UserProfileSerializer

from userprofile.models import UserProfile


class UserProfileAPI(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        instance = UserProfile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

