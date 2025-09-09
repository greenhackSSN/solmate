from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from rest_framework.response import Response
from usermgmt.models import CustomUser
from .models import TherapyPlan, SessionFeedback
from .serializers import TherapyPlanSerializer, SessionFeedbackSerializer
from .ai_match import match_patient_to_therapist
from rest_framework.decorators import permission_classes

# -------------------------------
# Therapy Plan API
# -------------------------------
class TherapyPlanViewSet(viewsets.ModelViewSet):
    queryset = TherapyPlan.objects.all()
    serializer_class = TherapyPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'therapist':
            raise PermissionError("Only therapists can create therapy plans")
        serializer.save(therapist=self.request.user)

    @action(detail=True, methods=['PATCH'], url_path='approve')
    def approve_plan(self, request, pk=None):
        plan = self.get_object()
        if request.user.role != 'supervisor':
            return Response({'error': 'Only supervisors can approve plans.'}, status=403)
        plan.status = 'approved'
        plan.save()
        return Response({'message': 'Therapy plan approved.', 'plan_id': plan.id})

# -------------------------------
# Session Feedback API
# -------------------------------
class SessionFeedbackViewSet(viewsets.ModelViewSet):
    queryset = SessionFeedback.objects.all()
    serializer_class = SessionFeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'therapist':
            raise PermissionError("Only therapists can add session feedback")
        serializer.save()

# -------------------------------
# AI Plan Suggestion API
# -------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ai_suggested_plan(patient):
    # Temporary placeholder until Vedha's API is ready
    return {
        "patient_id": patient.id,
        "suggested_plan": "Example plan (replace with AI output)"
    }

# -------------------------------
# Assign Patient API
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_patient(request):
    if request.user.role != 'supervisor':
        return Response({'error': 'Only supervisors can assign patients.'}, status=403)

    patient_id = request.data.get('patient_id')
    therapist_id = request.data.get('therapist_id')

    try:
        patient = CustomUser.objects.get(id=patient_id, role='patient')
        therapist = CustomUser.objects.get(id=therapist_id, role='therapist')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid patient or therapist ID.'}, status=400)

    # Optional: auto-create a therapy plan when assigning
    plan = TherapyPlan.objects.create(
        patient=patient,
        therapist=therapist,
        description='Assigned by supervisor',
        status='pending'
    )

    return Response({'message': 'Patient assigned to therapist.', 'plan_id': plan.id})

#--------------------------------
# Reports API
#--------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports_view(request):
    if request.user.role not in ['supervisor', 'therapist']:
        return Response({'error': 'Only supervisors or therapists can access reports.'}, status=403)

    # Total patients per therapist
    therapist_stats = CustomUser.objects.filter(role='therapist').annotate(
        total_patients=Count('therapyplan__patient', distinct=True)
    ).values('id', 'username', 'total_patients')

    # Total sessions completed per therapist
    sessions_stats = CustomUser.objects.filter(role='therapist').annotate(
        total_sessions=Count('therapyplan__sessionfeedback', distinct=True)
    ).values('id', 'username', 'total_sessions')

    # Average progress (example: avg plan status)
    avg_status = TherapyPlan.objects.filter(status='active').aggregate(avg_active=Avg('id'))

    # Best and worst therapy plans (by number of feedbacks)
    plan_feedbacks = TherapyPlan.objects.annotate(
        feedback_count=Count('sessionfeedback')
    ).order_by('-feedback_count')
    best_plan = plan_feedbacks.first()
    worst_plan = plan_feedbacks.last()

    data = {
        'therapist_stats': list(therapist_stats),
        'sessions_stats': list(sessions_stats),
        'average_active_plan_id': avg_status['avg_active'],
        'best_plan': {'id': best_plan.id, 'description': best_plan.description} if best_plan else None,
        'worst_plan': {'id': worst_plan.id, 'description': worst_plan.description} if worst_plan else None,
    }

    return Response(data)