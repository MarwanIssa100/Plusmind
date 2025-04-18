from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Therapist

class IsTherapist(BasePermission):
    def has_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user