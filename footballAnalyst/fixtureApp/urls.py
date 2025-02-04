from django.urls import path
from .views import FixtureView, RecentMatchesView, LiveMatchesView, UpcomingMatchesView
urlpatterns = [
    path('all/', FixtureView.as_view(), name='fixtures-list'),
    path('upcoming/', UpcomingMatchesView.as_view(), name='upcoming-matches'),
    path('recent/', RecentMatchesView.as_view(), name='recent-matches'),
    path('live/', LiveMatchesView.as_view(), name='live-matches'),
]
