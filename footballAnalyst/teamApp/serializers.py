from rest_framework import serializers
from .models import Player, Team

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id', 'name', 'position', 'matches_played', 'starts', 'goals', 'assists',
            'yellow_cards', 'red_cards', 'xG', 'xAG', 'progressive_carries', 
            'progressive_passes', 'save_percentage', 'clean_sheets', 'tackles_won', 'interceptions', 'crest', 'rating',
        ]

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
