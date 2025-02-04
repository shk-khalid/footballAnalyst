import pandas as pd
import os
from django.core.management.base import BaseCommand
from teamApp.models import Team, Player

class Command(BaseCommand):
    help = "Import player data from a CSV or Excel file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the data file (CSV or Excel)")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            # Detect file type and read data
            ext = os.path.splitext(file_path)[-1].lower()
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path)
            else:
                self.stdout.write(self.style.ERROR("Unsupported file format. Please provide a CSV or Excel file."))
                return

            # Replace NaN values with default values
            df = df.fillna(0)

            # Process each row
            for index, row in df.iterrows():
                try:
                    # Get or create the team and update the crest
                    team, created = Team.objects.update_or_create(
                        name=row['CLUB'],
                        defaults={'crest': row['CREST']}  # Store crest in Team model
                    )

                    # Ensure red cards are stored as integers
                    red_cards = int(float(row['CrdR'])) if row['CrdR'] else 0

                    # Ensure rating is converted to an integer
                    rating = int(float(row['RATING'])) if row['RATING'] else 0

                    # Insert or update player record
                    player, created = Player.objects.update_or_create(
                        name=row['NAME'],
                        team=team,
                        defaults={
                            "position": row['POSITION'],
                            "matches_played": int(row['MP']),
                            "starts": int(row['Starts']),
                            "goals": int(row['Gls']),
                            "assists": int(row['Ast']),
                            "yellow_cards": int(row['CrdY']),
                            "red_cards": red_cards,
                            "xG": float(row['xG']),
                            "xAG": float(row['xAG']),
                            "progressive_carries": int(row['PrgC']),
                            "progressive_passes": int(row['PrgP']),
                            "save_percentage": float(row['SAVE%']) if row['SAVE%'] else None,
                            "clean_sheets": int(row['CS']) if row['CS'] else None,
                            "tackles_won": int(row['TKLW']) if row['TKLW'] else None,
                            "interceptions": int(row['INT']) if row['INT'] else None,
                            "rating": rating,
                            "crest": row['CREST'],
                        }
                    )

                    action = "Added" if created else "Updated"
                    self.stdout.write(self.style.SUCCESS(f"{action}: {player.name} ({team.name})"))

                except Exception as row_error:
                    self.stdout.write(self.style.ERROR(f"Error processing row {index + 1}: {row_error}"))

            self.stdout.write(self.style.SUCCESS("Player data imported successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
