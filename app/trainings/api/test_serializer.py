from rest_framework import serializers


class WordCardTrainingSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    type = serializers.CharField(allow_null=True, required=False)
    word = serializers.CharField()
    options = serializers.ListSerializer(child=serializers.CharField())

