from rest_framework import serializers
from .models import TherapyPlan, SessionFeedback

class TherapyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapyPlan
        fields = '__all__'

class SessionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionFeedback
        fields = '__all__'
