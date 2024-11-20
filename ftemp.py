
# input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 
import pandas as pd
import tkinter as tk
from tkinter import ttk

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
    
    return summary

def display_summary(summary):
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Summary Output")

    # Add a Text widget to display the data
    text_widget = tk.Text(root, wrap="none", font=("Courier", 10), padx=10, pady=10)
    text_widget.pack(fill="both", expand=True)

    # Insert formatted summary data into the Text widget
    previous_date = None
    for _, row in summary.iterrows():
        if row['Date'] != previous_date:
            if previous_date is not None:  # Add a blank line for date change
                text_widget.insert(tk.END, "\n")
            previous_date = row['Date']
        text_widget.insert(
            tk.END, 
            f"{row['Date']: <12} {row['Tags']: <20} {row['Duration']:.2f} {row['Project']}\n"
        )

    # Make the text read-only
    text_widget.configure(state="disabled")

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv'   
    summary_data = process_data(input_file)
    display_summary(summary_data)
