from rest_framework import serializers
from .models import Article

from chemie.customprofile.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    author = UserSerializer()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = Article
        fields = "__all__"
