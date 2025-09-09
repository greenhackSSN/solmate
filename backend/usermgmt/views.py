from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from usermgmt.models import CustomUser
from therapyapp.models import TherapyPlan

# ---------------------------
# Signup view
# ---------------------------
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

# ---------------------------
# Login view using JWT
# ---------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ---------------------------
# Step 14: Supervisor assigns patient
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_patient(request):
    # Only supervisors can assign
    if request.user.role != 'supervisor':
        return Response({'error': 'Only supervisors can assign patients.'}, status=403)

    patient_id = request.data.get('patient_id')
    therapist_id = request.data.get('therapist_id')

    try:
        patient = CustomUser.objects.get(id=patient_id, role='patient')
        therapist = CustomUser.objects.get(id=therapist_id, role='therapist')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid patient or therapist ID.'}, status=404)

    # Create an empty therapy plan placeholder (status = pending)
    plan = TherapyPlan.objects.create(
        patient=patient,
        therapist=therapist,
        description='Pending therapy plan',
        status='pending'
    )

    return Response({
        'message': 'Patient assigned successfully.',
        'plan_id': plan.id,
        'patient': patient.username,
        'therapist': therapist.username
    })
