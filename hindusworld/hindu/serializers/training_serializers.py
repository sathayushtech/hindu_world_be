from rest_framework import serializers
from ..models import Training
from ..utils import image_path_to_binary

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"



class TrainingSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Training
        fields = ['status']        
