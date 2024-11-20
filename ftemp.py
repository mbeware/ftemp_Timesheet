import pandas as pd


# Convert Duration from HH:MM:SS to total seconds
def duration_to_seconds(duration):
    h, m, s = map(int, duration.split(':'))
    return h * 3600 + m * 60 + s

# Load the uploaded CSV file to inspect its structure
file_path = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv'
data = pd.read_csv(file_path)




data['Duration (seconds)'] = data['Duration'].apply(duration_to_seconds)

# Summarize the total duration grouped by Date, Tags, and Project
summary = data.groupby(['Date', 'Tags', 'Project'])['Duration (seconds)'].sum().reset_index()

# Convert the total duration back to HH:MM:SS format for readability
def seconds_to_hms(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

summary['Total Duration'] = summary['Duration (seconds)'].apply(seconds_to_hms)

# Drop the raw seconds column for clarity
summary = summary.drop(columns=['Duration (seconds)'])

print(summary)
