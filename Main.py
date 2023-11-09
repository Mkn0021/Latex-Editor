import tkinter as tk
from tkinter import ttk, messagebox
from Asset.LabReportUI_handler import LabReportUI_handler

class LabReportUI:
    def __init__(self):

        # Create instance of LabReportEditor
        self.lab_report = LabReportUI_handler(self)
        # Create and configure widgets
        self.create_entry_window()


    def create_entry_window(self):
        self.lab_report.set_default_style("Latex Editor")

        # File path entry
        file_path_label = ttk.Label(self.lab_report.window, text="Previous File Path:")
        file_path_label.grid(row=3, column=1, pady=10, padx=10)
        file_path_entry = ttk.Entry(self.lab_report.window)
        file_path_entry.grid(row=3, column=2, pady=5, padx=10)

        # Browse button
        browse_button = ttk.Button(self.lab_report.window, text="Browse", command=lambda: self.lab_report.browse_file(file_path_entry))
        browse_button.grid(row=3, column=3, pady=5, padx=10)

        # Experiment Name entry
        experiment_name_label = ttk.Label(self.lab_report.window, text="Experiment Name:")
        experiment_name_label.grid(row=4, column=1, pady=10, padx=10)
        experiment_name_entry = ttk.Entry(self.lab_report.window)
        experiment_name_entry.grid(row=4, column=2, pady=10, padx=10)

        # Edit button
        edit_button = ttk.Button(self.lab_report.window, text="Enter", command=lambda: self.lab_report.edit_title(file_path_entry, experiment_name_entry))
        edit_button.grid(row=4, column=3, pady=10, padx=10)

        # Bind Enter key to the edit_title function
        self.lab_report.window.bind("<Return>", lambda event: self.lab_report.edit_title(file_path_entry, experiment_name_entry))

        # Create progressbar
        self.lab_report.create_progressbar()

        self.lab_report.window.mainloop()
        
    

    def create_image_adder_window(self):
        try:
            self.lab_report.set_default_style("Image Adder")

            self.lab_report.window.grid_columnconfigure(0, minsize=95)  # Add a margin on the left

            # Instruction Label
            instruction_text = "How many images do you want to add in one row? (Enter numbers separated by space)"
            instruction_label = ttk.Label(self.lab_report.window, text=instruction_text)
            instruction_label.grid(row=3, column=1, columnspan=3, pady=10)

            # Num of Image entry
            initial_label_text = f"{self.lab_report.sections_with_image[self.lab_report.index]}:"
            num_images_label = ttk.Label(self.lab_report.window, text=initial_label_text, font=("Helvetica", 14, "bold"))
            num_images_label.grid(row=4, column=1, pady=10, sticky=tk.W)
            num_images_entry = ttk.Entry(self.lab_report.window, width=50)
            num_images_entry.grid(row=5, column=1 , pady=5)

            # Edit button
            self.edit_button = ttk.Button(self.lab_report.window, text="Enter", command=lambda: self.lab_report.image_adder(num_images_entry, num_images_label))
            self.edit_button.grid(row=5, column=2, pady=5)

            # Bind Enter key to the same function
            self.lab_report.window.bind("<Return>", lambda event: self.lab_report.image_adder(num_images_entry, num_images_label))

            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in image adder window: {str(e)}")
    
        

    def create_graph_adder_window(self):
        try:
            self.lab_report.set_default_style("Graph Adder" )

            self.lab_report.window.grid_columnconfigure(0, minsize=120)

            #introduction text
            introduction_label = ttk.Label(self.lab_report.window , text = "Enter the data (space separeted) Like : (2.1 3.2 4.5 )")
            introduction_label.grid(row=2, column=1, columnspan=2, pady=5, padx=10)

            # X-axis label entry
            x_label_label = ttk.Label(self.lab_report.window, text="Enter x-axis label:")
            x_label_label.grid(row=3, column=1, pady=5, padx=10, sticky=tk.E)
            x_label_entry = ttk.Entry(self.lab_report.window)
            x_label_entry.grid(row=3, column=2, pady=5, padx=10)

            # Y-axis label entry
            y_label_label = ttk.Label(self.lab_report.window, text="Enter y-axis label:")
            y_label_label.grid(row=4, column=1, pady=5, padx=10, sticky=tk.E)
            y_label_entry = ttk.Entry(self.lab_report.window)
            y_label_entry.grid(row=4, column=2, pady=5, padx=10)


            # X data entry
            x_data_label = ttk.Label(self.lab_report.window, text="Enter x-axis data :")
            x_data_label.grid(row=5, column=1, pady=5, padx=10)
            x_data_entry = ttk.Entry(self.lab_report.window)
            x_data_entry.grid(row=5, column=2, pady=5, padx=10)

            # Y data entry
            y_data_label = ttk.Label(self.lab_report.window, text="Enter y-axis data :")
            y_data_label.grid(row=6, column=1, pady=5, padx=10)
            y_data_entry = ttk.Entry(self.lab_report.window)
            y_data_entry.grid(row=6, column=2, pady=5, padx=10)

            # Checkbox for adding more data series
            add_series_var = tk.BooleanVar()
            add_series_checkbox = ttk.Checkbutton(self.lab_report.window, text="Add more data series", variable=add_series_var , command=lambda: self.toggle_data_series_entry(add_series_var, add_series_checkbox , num_of_extraDataseries_entry))
            add_series_checkbox.grid(row=7, column=1, columnspan=2, pady=10)

            num_of_extraDataseries_entry = ttk.Entry(self.lab_report.window , width= 32 )


            # Button to submit data
            submit_button = ttk.Button(self.lab_report.window, text="Submit", command=lambda: self.lab_report.graph_adder( x_label_entry.get() , x_data_entry, y_label_entry.get(), y_data_entry, add_series_var , num_of_extraDataseries_entry.get()))
            submit_button.grid(row=8, column=1, columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in graph adder windows: {str(e)}")
    
    def toggle_data_series_entry(self, add_series_var, add_series_checkbox , num_of_extraDataseries_entry ):
    # Toggle visibility of widgets based on the checkbox state
        if add_series_var.get():
            add_series_checkbox.destroy()
        #Number of Extra data series
        num_of_extraDataseries_label = ttk.Label(self.lab_report.window, text="Number of extra Data Series :")
        num_of_extraDataseries_label.grid(row=7,  column=1, columnspan=2, pady=5, padx=10 , sticky=tk.W)
        num_of_extraDataseries_entry.grid(row=7,  column=1, columnspan=2, pady=5, padx=10 , sticky= tk.E )

        

    def create_data_entry_window(self):
        try:
            self.lab_report.set_default_style("Data Entry" )

            self.lab_report.window.grid_columnconfigure(0, minsize=120)

            # X data entry
            x_data_label = ttk.Label(self.lab_report.window, text="Enter X data (space-separated):")
            x_data_label.grid(row=3, column=1, pady=5, padx=10)
            x_data_series_entry = ttk.Entry(self.lab_report.window, width=30)
            x_data_series_entry.grid(row=3, column=2, pady=5, padx=10)

            # Y data entry
            y_data_label = ttk.Label(self.lab_report.window, text="Enter Y data (space-separated):")
            y_data_label.grid(row=4, column=1, pady=5, padx=10)
            y_data_series_entry = ttk.Entry(self.lab_report.window, width=30)
            y_data_series_entry.grid(row=4, column=2, pady=5, padx=10)

            #x_data_series_entry.bind("<Return>", lambda event: y_data_series_entry.focus() if y_data_series_entry else self.lab_report.handle_data_entry(x_data_series_entry, y_data_series_entry))
            #y_data_series_entry.bind("<Return>", lambda event: self.lab_report.handle_data_entry(x_data_series_entry, y_data_series_entry))

            # Button to submit data
            submit_button = ttk.Button(self.lab_report.window, text="Submit",command=lambda: self.lab_report.handle_data_entry(x_data_series_entry, y_data_series_entry))
            submit_button.grid(row=5, column=1, columnspan=2, pady=20)

            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in create data entry windows : {str(e)}")


#Create Lab Report 
Lab_Report = LabReportUI()
