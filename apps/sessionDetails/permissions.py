from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPatientOrTherapist(BasePermission):
    """Custom permission to only allow patients or therapists of the session to view it"""
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is either the patient or therapist of the session
        return request.user == obj.patient_id.user or request.user == obj.therapist_id.user