import requests
import json
import os
from datetime import datetime, timedelta
from django.conf import settings

class HMSAPI:
    """100ms.live API integration for video conferencing"""
    
    def __init__(self):
        self.base_url = "https://api.100ms.live/v2"
        self.app_id = getattr(settings, 'HMS_APP_ID', os.environ.get('HMS_APP_ID'))
        self.app_secret = getattr(settings, 'HMS_APP_SECRET', os.environ.get('HMS_APP_SECRET'))
        self.template_id = getattr(settings, 'HMS_TEMPLATE_ID', os.environ.get('HMS_TEMPLATE_ID'))
        self.manager_id = getattr(settings, 'HMS_MANAGER_ID', os.environ.get('HMS_MANAGER_ID'))
        
        if not all([self.app_id, self.app_secret, self.template_id]):
            raise ValueError("HMS_APP_ID, HMS_APP_SECRET, and HMS_TEMPLATE_ID must be configured")
    
    def _get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self.manager_id}',
            'Content-Type': 'application/json'
        }
    
    def create_room(self, room_name, description=None, max_participants=2 , max_duration_seconds = 3600):   
        """Create a new room in 100ms.live"""
        url = f"{self.base_url}/rooms"
        
        payload = {
            "name": room_name,
            "description": description or f"Therapy session room: {room_name}",
            "template_id": self.template_id,
            "max_participants": max_participants
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create room: {str(e)}")
    
    def get_room(self, room_id):
        """Get room details"""
        url = f"{self.base_url}/rooms/{room_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get room: {str(e)}")
    
    def generate_token(self, room_id, user_id, user_name, role="host"):
        """Generate authentication token for a user"""
        url = f"{self.base_url}/token"
        
        payload = {
            "room_id": room_id,
            "user_id": user_id,
            "role": role,
            "user_name": user_name
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate token: {str(e)}")
    
    def get_room_url(self, room_id, room_code):
        """Generate room URL for joining"""
        return f"https://app.100ms.live/meeting/{room_code}"
    
    def deactivate_room(self, room_id):
        """Deactivate a room"""
        url = f"{self.base_url}/rooms/{room_id}/deactivate"
        
        try:
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to deactivate room: {str(e)}")
    
    def get_active_peers(self, room_id):
        """Get active participants in a room"""
        url = f"{self.base_url}/rooms/{room_id}/peers"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get active peers: {str(e)}") 