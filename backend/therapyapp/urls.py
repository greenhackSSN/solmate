from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TherapyPlanViewSet, SessionFeedbackViewSet, ai_match, assign_patient, reports_view

router = DefaultRouter()
router.register(r'therapyplans', TherapyPlanViewSet, basename='therapyplan')
router.register(r'feedbacks', SessionFeedbackViewSet, basename='sessionfeedback')

urlpatterns = [
    path('', include(router.urls)),
    path('assign_patient/', assign_patient, name='assign-patient'),
    path('reports/', reports_view, name='reports'),
    path('ai_plan_suggestion/<int:patient_id>/', ai_plan_suggestion, name='ai-plan-suggestion'),
]
