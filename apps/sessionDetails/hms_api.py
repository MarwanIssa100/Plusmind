import requests
import json
import os
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import uuid

class HMSAPI:
    """100ms.live API integration for video conferencing"""
    
    def __init__(self):
        self.base_url = "https://api.100ms.live/v2"
        self.app_id = getattr(settings, 'HMS_APP_ID')
        self.app_secret = getattr(settings, 'HMS_APP_SECRET')
        self.template_id = getattr(settings, 'HMS_TEMPLATE_ID')
        if not all([self.app_id, self.app_secret, self.template_id]):
            raise ValueError("HMS_APP_ID, HMS_APP_SECRET, and HMS_TEMPLATE_ID must be configured")
    

    def _generate_jwt(self):
        payload = {
            "access_key": self.app_id,
            "type": "management",
            "version": 2,
            "jti": str(uuid.uuid4()),
            "iat": int(datetime.utcnow().timestamp()),
            "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp())
        }
        token = jwt.encode(payload, self.app_secret, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    def _get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self._generate_jwt()}',
            'Content-Type': 'application/json'
        }
    
    def create_room(self, room_name, description=None, max_participants=2 , max_duration_seconds = 3600):   
        """Create a new room in 100ms.live"""
        url = f"{self.base_url}/rooms"
        
        payload = {
            "name": room_name,
            "description": description or f"Therapy session room: {room_name}",
            "template_id": self.template_id
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise Exception(f"Failed to create room: {str(e)}")

    def create_room_code(self, room_id):
        """Create a room code for a room"""
        url = f"{self.base_url}/room-codes/room/{room_id}"
        
        try:
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create room code: {str(e)}")
    
    def get_room_codes(self, room_id):
        """Get room codes for a room"""
        url = f"{self.base_url}/room-codes/room/{room_id}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get room codes: {str(e)}")

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