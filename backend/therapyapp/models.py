from django.db import models
from django.conf import settings

class TherapyPlan(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plans")
    therapist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="therapist_plans")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")  # pending, approved, active

class SessionFeedback(models.Model):
    plan = models.ForeignKey(TherapyPlan, on_delete=models.CASCADE, related_name="feedbacks")
    feedback = models.TextField()
    progress_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
