from django.urls import path
from .views import TeamView, TeamList


urlpatterns = [
    path('<int:team_id>/players/', TeamView.as_view(), name='team-players-list'),
    path('all/', TeamList.as_view(), name='team-list'),
]
