from django.urls import path, include

urlpatterns = [
    
    path('team/', include(('teamApp.urls'))),
    path("match/", include("fixtureApp.urls")),
]
