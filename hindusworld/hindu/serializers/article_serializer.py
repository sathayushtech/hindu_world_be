from rest_framework import serializers
from ..models import Article
from ..utils import image_path_to_binary  # Import the utility function



class ArticleSerializer(serializers.ModelSerializer):
    article = serializers.CharField(required=False)

    class Meta:
        model = Article
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['article'] = image_path_to_binary(instance.article)
        return representation



# class ArticleSerializer(serializers.ModelSerializer):
#     image = serializers.CharField(required=False)
#     article = serializers.CharField(required=False)

#     class Meta:
#         model = Article
#         fields = "__all__"

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['image'] = image_path_to_binary(instance.image)
#         representation['article'] = image_path_to_binary(instance.article)
#         return representation


