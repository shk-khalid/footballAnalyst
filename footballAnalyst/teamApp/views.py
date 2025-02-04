from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Team, Player
from .serializers import PlayerSerializer, TeamSerializer

class TeamView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
            
            players = Player.objects.filter(team=team)

            paginator = PageNumberPagination()
            paginator.page_size = 5  # Display 5 players per page
            result_page = paginator.paginate_queryset(players, request)
            
            serializer = PlayerSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Team.DoesNotExist:
            return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        
class TeamList(APIView):
    def get(self, request):
        try:
            # team = Team.objects.get(id=team_id)
            team = Team.objects.all()
            
            # players = Player.objects.filter(team=team)

            paginator = PageNumberPagination()
            paginator.page_size = 20  # Display 5 players per page
            result_page = paginator.paginate_queryset(team, request)
            
            serializer = TeamSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
        except Team.DoesNotExist:
            return Response({"error": "TeamList not found"}, status=status.HTTP_404_NOT_FOUND)