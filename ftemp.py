
# input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 
import pandas as pd
import tkinter as tk
from tkinter import ttk
import os

# Helper function to convert duration
def duration_to_decimal(duration):
    """Convert HH:MM:SS duration to a decimal hour representation."""
    h, m, s = map(int, duration.split(':'))
    return h + m / 60 + s / 3600

# Helper function to process the data
def process_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
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

# Function to update the Treeview with new data
def update_tree(tree, summary):
    # Clear the Treeview
    for item in tree.get_children():
        tree.delete(item)

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

# Function to navigate files
def change_file(direction, current_file, tree, folder_path):
    files = sorted(f for f in os.listdir(folder_path) if f.endswith('.csv'))
    try:
        current_index = files.index(os.path.basename(current_file))
    except ValueError:
        return

    if direction == "previous" and current_index > 0:
        new_file = os.path.join(folder_path, files[current_index - 1])
    elif direction == "next" and current_index < len(files) - 1:
        new_file = os.path.join(folder_path, files[current_index + 1])
    else:
        return  # No change

    summary = process_data(new_file)
    update_tree(tree, summary)
    tree.master.title(f"Summary Table - {os.path.basename(new_file)}")  # Update window title

# Main display function
def display_summary(file_path):
    folder_path = os.path.dirname(file_path)
    summary = process_data(file_path)

    # Create the main Tkinter window
    root = tk.Tk()
    root.title(f"Summary Table - {os.path.basename(file_path)}")

    # Create a Treeview widget
    columns = ["Date", "Tags", "Duration", "Project"]
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

    # Define column headings
    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, anchor="w", width=150)

    # Insert initial data
    update_tree(tree, summary)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Add navigation buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)

    prev_btn = tk.Button(btn_frame, text="Previous File", command=lambda: change_file("previous", file_path, tree, folder_path))
    prev_btn.pack(side="left", padx=5)

    next_btn = tk.Button(btn_frame, text="Next File", command=lambda: change_file("next", file_path, tree, folder_path))
    next_btn.pack(side="left", padx=5)

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 
    display_summary(input_file)

