
input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 

import pandas as pd

# File path
input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 

def duration_to_decimal(duration):
    """Convert HH:MM:SS duration to a decimal hour representation."""
    h, m, s = map(int, duration.split(':'))
    return h + m / 60 + s / 3600

def process_data(input_path):
    # Load the CSV file
    data = pd.read_csv(input_path)
    
    # Convert Duration to decimal format
    data['Duration (decimal hours)'] = data['Duration'].apply(duration_to_decimal)
    
    # Summarize the data
    summary = data.groupby(['Date', 'Tags', 'Project'])['Duration (decimal hours)'].sum().reset_index()
    
    # Format the DataFrame
    summary = summary.rename(columns={'Duration (decimal hours)': 'Duration'})
    summary = summary[['Date', 'Tags', 'Duration', 'Project']]
    
    # Insert blank lines where the date changes and print to console
    previous_date = None
    for _, row in summary.iterrows():
        if row['Date'] != previous_date:
            if previous_date is not None:  # Avoid blank line at the top
                print()  # Print a blank line
            previous_date = row['Date']
        print(f"{row['Date']: <12} {row['Tags']: <20} {row['Duration']:.2f} {row['Project']}")

# Run the script
if __name__ == "__main__":
    process_data(input_file)
