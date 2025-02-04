import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
file_path = r'C:\Users\ks785\Downloads\PLAYERS.csv'
data = pd.read_csv(file_path)

# Initialize MinMaxScaler for normalizing stats
scaler = MinMaxScaler()

# Columns to normalize
stats_to_normalize = ['G+A', 'xG', 'xAG', 'PrgC', 'PrgP', 'SAVE%', 'CS', 'TKLW', 'INT', 'CrdY', 'CrdR']

# Make a copy of columns to normalize
normalized_data = data[stats_to_normalize].copy()

# Normalize the copied columns and handle missing values
normalized_data = scaler.fit_transform(normalized_data.fillna(0))

# Replace the original columns with normalized ones in the copied DataFrame
normalized_data = pd.DataFrame(normalized_data, columns=stats_to_normalize)

# Add the normalized data back to the original DataFrame without affecting other fields
for col in stats_to_normalize:
    data[col] = normalized_data[col]

# Function to calculate ratings based on position
def calculate_rating(row):
    if row['POSITION'] == 'GK':
        # Goalkeeper rating formula
        rating = (row['SAVE%'] * 0.5 + row['CS'] * 0.3 - row['CrdY'] * 0.1 - row['CrdR'] * 0.1)
    elif row['POSITION'] == 'DF':
        # Defender rating formula
        rating = (row['TKLW'] * 0.4 + row['INT'] * 0.3 + row['PrgC'] * 0.2 - row['CrdY'] * 0.05 - row['CrdR'] * 0.05)
    elif row['POSITION'] == 'MF':
        # Midfielder rating formula
        rating = (row['G+A'] * 0.4 + row['xG'] * 0.2 + row['xAG'] * 0.2 + row['PrgP'] * 0.1 - row['CrdY'] * 0.05 - row['CrdR'] * 0.05)
    elif row['POSITION'] == 'FW':
        # Forward rating formula
        rating = (row['G+A'] * 0.5 + row['xG'] * 0.3 + row['xAG'] * 0.2)
    else:
        # Default rating for unknown positions
        rating = 0
    # Scale rating to 1-10 and round to one decimal place
    return round(max(1, min(10, rating * 10)), 1)

# Apply the rating calculation
data['RATING'] = data.apply(calculate_rating, axis=1)

# Save the updated DataFrame
output_path = r'C:\Users\ks785\Downloads\UPDATED_PLAYERS.csv'
data.to_csv(output_path, index=False)

print(f"Ratings have been calculated and stored in the file: {output_path}")
