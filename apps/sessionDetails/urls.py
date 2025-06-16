from django.urls import path
from .views import (
    SessionCreateViewset, 
    search,
    DeleteSessionView,
    GetAllSessionsView,
    RetrieveSessionView,
    UpdateSessionTimeView
)

app_name = 'sessionDetails'

urlpatterns = [
    path('create/', SessionCreateViewset.as_view(), name='session-create'),
    path('search/', search, name='search'),
    path('delete/<int:pk>/', DeleteSessionView.as_view(), name='session-delete'),
    path('all/', GetAllSessionsView.as_view(), name='all-sessions'),
    path('session/<int:pk>/', RetrieveSessionView.as_view(), name='session-detail'),
    path('update/<int:pk>/', UpdateSessionTimeView.as_view(), name='session-update'),
]
