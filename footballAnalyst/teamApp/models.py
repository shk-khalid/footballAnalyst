from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    crest = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    matches_played = models.PositiveIntegerField(default=0)
    starts = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_cards = models.PositiveIntegerField(default=0)
    xG = models.FloatField(default=0.0)  # Expected Goals
    xAG = models.FloatField(default=0.0)  # Expected Assist Goals
    progressive_carries = models.PositiveIntegerField(default=0)
    progressive_passes = models.PositiveIntegerField(default=0)
    save_percentage = models.FloatField(default=0.0, null=True, blank=True)  # Goalkeepers only
    clean_sheets = models.PositiveIntegerField(default=0, null=True, blank=True)  # Goalkeepers only
    tackles_won = models.PositiveIntegerField(default=0, null=True, blank=True)  # Midfielders and Defenders
    interceptions = models.PositiveIntegerField(default=0, null=True, blank=True)  # Midfielders and Defenders

    crest = models.CharField(max_length=255, null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
