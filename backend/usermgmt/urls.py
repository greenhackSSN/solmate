from django.urls import path
from .views import SignupView, MyTokenObtainPairView, assign_patient
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('assign-patient/', assign_patient, name='assign_patient'),
]
