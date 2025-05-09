from rest_framework import serializers
from .models import SessionDetails
from datetime import timedelta
class SessionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDetails
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['duration'] == "30":
            end_time = validated_data['start_time'] + timedelta(minutes=30)
        else:
            end_time = validated_data['start_time'] + timedelta(minutes=60)

        session = SessionDetails.objects.create(
            session_type = validated_data['session_type'],
            patient_id = validated_data.get('patient_id',self.context['request'].user.id),
            therapist_id = validated_data.get('therapist_id'),
            start_time = validated_data['start_time'],
            end_time = end_time,
            duration = validated_data['duration'],
        )
        return session

