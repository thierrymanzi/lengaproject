from rest_framework import serializers

from ..models import (LesssonTracking, QuestionTracking,
                      CategoryTracking
                      )


class LessonTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LesssonTracking
        fields = '__all__'


class QuestionTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTracking
        fields = '__all__'

class CategoryTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTracking
        fields = '__all__'
