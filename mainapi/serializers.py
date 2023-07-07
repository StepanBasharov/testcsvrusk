from rest_framework import serializers
from .models import User, Trade


class UploadDetailsSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
