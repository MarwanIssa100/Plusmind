from django.urls import path
from .views import (
    SessionCreateViewset, 
    search,
    DeleteSessionView,
    GetAllSessionsView,
    RetrieveSessionView,
    UpdateSessionTimeView,
    VideoRoomView,
    VideoTokenView,
    EnableVideoView,
    RoomParticipantsView
)

app_name = 'sessionDetails'

urlpatterns = [
    path('create/', SessionCreateViewset.as_view(), name='session-create'),
    path('search/', search, name='search'),
    path('delete/<int:pk>/', DeleteSessionView.as_view(), name='session-delete'),
    path('all/', GetAllSessionsView.as_view(), name='all-sessions'),
    path('<int:pk>/', RetrieveSessionView.as_view(), name='session-detail'),
    path('update/<int:pk>/', UpdateSessionTimeView.as_view(), name='session-update'),
    
    # Video conferencing endpoints
    path('video/room/<int:pk>/', VideoRoomView.as_view(), name='video-room'),
    path('video/token/<int:pk>/', VideoTokenView.as_view(), name='video-token'),
    path('video/enable/<int:pk>/', EnableVideoView.as_view(), name='enable-video'),
    path('video/participants/<int:pk>/', RoomParticipantsView.as_view(), name='room-participants'),
]
