
# input_file = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\6007_Boarhub_902_informatique_3055_PATBQ_4051_VSP_20241120135529.csv' 
import pandas as pd
import tkinter as tk
from tkinter import ttk

import os

class ft:
    def __init__(self):
        self.ftempFolder = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\' 
        Allfiles = sorted(f for f in os.listdir(self.ftempFolder) if f.endswith('.csv'))
        LastFile = os.path.join(self.ftempFolder, Allfiles[-1])
        self.display_summary(LastFile)


    # Helper function to convert duration
    def duration_to_decimal(self,duration):
        """Convert HH:MM:SS duration to a decimal hour representation."""
        h, m, s = map(int, duration.split(':'))
        return h + m / 60 + s / 3600

    # Helper function to process the data
    def process_data(self,file_path):
        # Load the CSV file
        data = pd.read_csv(file_path)
        
        # Convert Duration to decimal format
        data['Duration (decimal hours)'] = data['Duration'].apply(self.duration_to_decimal)
        
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
    def update_tree(self, summary):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

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
            self.tree.insert("", "end", values=values, tags=(tag,))

        # Apply row styles
        self.tree.tag_configure("even", background=light_yellow)
        self.tree.tag_configure("odd", background=dark_yellow)
        self.tree.tag_configure("blank", background=light_gray)

    # Function to navigate files
    def change_file(self,event):
        cs = self.fileChoiceList.curselection()
        f = self.Allfiles[cs[0]]
        new_file = os.path.join(self.ftempFolder, f )

        summary = self.process_data(new_file)
        self.update_tree( summary)
        self.tree.master.title(f"Summary Table - {os.path.basename(new_file)}")  # Update window title

    # Main display function
    def display_summary(self,file_path):
        
        folder_path = os.path.dirname(file_path)
        self.summary = self.process_data(file_path)

        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title(f"Summary Table - {os.path.basename(file_path)}")

        # Create a Treeview widget
        columns = ["Date", "Tags", "Duration", "Project"]
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)

        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=150)

        # Insert initial data
        self.update_tree(self.summary)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # # Add navigation buttons
        select_frame = tk.Frame(self.root)
        select_frame.pack(fill="x", padx=10, pady=10)

        self.ftempFolder = 'C:\\Users\\mbelanger\\OneDrive - CDPQ\\perso\\ftemps\\' 
        self.Allfiles = sorted(f for f in os.listdir(self.ftempFolder) if f.endswith('.csv'))
    
        fileChoiceListvar = tk.StringVar()
        fileChoiceListvar.set(self.Allfiles)

        self.fileChoiceList = tk.Listbox(select_frame, listvariable=fileChoiceListvar, selectmode='browse')
        self.fileChoiceList.bind('<<ListboxSelect>>', self.change_file)
        self.fileChoiceList.pack(side="left", padx=5)

        # next_btn = tk.Button(btn_frame, text="Next File", command=lambda: change_file("next", file_path, tree, folder_path))
        # next_btn.pack(side="left", padx=5)

    def run(self):
        # Run the Tkinter main loop
        self.root.mainloop()

if __name__ == "__main__":
    ft().run()

