import os
import requests
import pytz
from datetime import datetime
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Load environment variables
load_dotenv()

API_KEY = os.getenv("FOOTBALL-DATA.ORG_APIKEY")

# Helper function to fetch match data
def fetch_matches():
    url = 'https://api.football-data.org/v4/competitions/PL/matches'
    headers = {'X-Auth-Token': API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('matches', [])
    except requests.exceptions.RequestException as e:
        raise Exception("Error fetching matches: {}".format(str(e)))

# Helper function to filter matches
def filter_matches(matches, now, status=None, upcoming=False, recent=False):
    utc_timezone = pytz.UTC
    filtered_matches = []

    for match in matches:
        match_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc_timezone)

        # Filter based on the provided criteria
        if status and match.get('status') == status:
            filtered_matches.append(match)
        elif upcoming and match_date > now and match.get('status') in ['SCHEDULED']:
            filtered_matches.append(match)
        elif recent and match_date < now and match.get('status') in ['FINISHED', 'IN_PLAY', 'PAUSED']:
            filtered_matches.append(match)

    # Sort matches by recency
    if upcoming:
        filtered_matches.sort(key=lambda m: m['utcDate'])  # Ascending order for upcoming
    elif recent:
        filtered_matches.sort(key=lambda m: m['utcDate'], reverse=True)  # Descending order for recent

    return filtered_matches

# Base View
class BaseFixtureView(APIView):
    def fetch_and_filter(self, status=None, upcoming=False, recent=False):
        try:
            matches = fetch_matches()
            now = datetime.now(pytz.UTC)
            return filter_matches(matches, now, status=status, upcoming=upcoming, recent=recent)
        except Exception as e:
            return {"error": str(e)}

# Fixture View (All Matches Segregated)
class FixtureView(BaseFixtureView):
    def get(self, request):
        try:
            live_matches = self.fetch_and_filter(status='LIVE')
            recent_matches = self.fetch_and_filter(recent=True)
            upcoming_matches = self.fetch_and_filter(upcoming=True)

            return Response({
                'upcoming': upcoming_matches,
                'recent': recent_matches,
                'live': live_matches,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Upcoming Matches View
class UpcomingMatchesView(BaseFixtureView):
    def get(self, request):
        try:
            upcoming_matches = self.fetch_and_filter(upcoming=True)
            return Response(upcoming_matches, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Recent Matches View
class RecentMatchesView(BaseFixtureView):
    def get(self, request):
        try:
            recent_matches = self.fetch_and_filter(recent=True)
            return Response(recent_matches, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Live Matches View
class LiveMatchesView(BaseFixtureView):
    def get(self, request):
        try:
            live_matches = self.fetch_and_filter(status='LIVE')
            return Response(live_matches, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
