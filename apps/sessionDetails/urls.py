from django.urls import path
from .views import SessionCreateViewset, search

app_name = 'sessionDetails'

urlpatterns = [
    path('create/', SessionCreateViewset.as_view(), name='session-create'),
    path('search/', search, name='search'),
]
