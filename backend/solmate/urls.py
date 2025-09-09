from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from therapyapp.views import TherapyPlanViewSet, SessionFeedbackViewSet, ai_match
from usermgmt.views import SignupView, MyTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'therapyplans', TherapyPlanViewSet)
router.register(r'feedbacks', SessionFeedbackViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('therapyapp.urls')),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('api/ai_match/<int:patient_id>/', ai_match, name='ai-match'),
]
