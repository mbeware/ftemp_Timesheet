
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
    
    # Add blank rows for date changes
    formatted_data = []
    previous_date = None
    for _, row in summary.iterrows():
        if row['Date'] != previous_date:
            if previous_date is not None:  # Insert a blank row
                formatted_data.append({'Date': '', 'Tags': '', 'Duration': '', 'Project': ''})
            previous_date = row['Date']
        formatted_data.append(row.to_dict())
    
    return pd.DataFrame(formatted_data)

def display_summary(summary):
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Summary Table")

    # Create a Treeview widget
    columns = ["Date", "Tags", "Duration", "Project"]
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

    # Define column headings
    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, anchor="w", width=150)

    # Define alternating row colors
    light_yellow = "#FFFACD"
    dark_yellow = "#FFD700"
    light_gray = "#D3D3D3"

    # Insert rows into the Treeview
    for idx, row in summary.iterrows():
        values = (row['Date'], row['Tags'], f"{row['Duration']:.2f}" if row['Duration'] else '', row['Project'])
        if row['Date'] == '':  # Blank rows
            tag = "blank"
        else:
            tag = "even" if idx % 2 == 0 else "odd"
        tree.insert("", "end", values=values, tags=(tag,))

    # Apply row styles
    tree.tag_configure("even", background=light_yellow)
    tree.tag_configure("odd", background=dark_yellow)
    tree.tag_configure("blank", background=light_gray)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 
    summary_data = process_data(input_file)
    display_summary(summary_data)
