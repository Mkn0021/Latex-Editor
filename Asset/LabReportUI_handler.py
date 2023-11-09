from datetime import datetime, timedelta
import re ,shutil , os , subprocess
import tkinter as tk
from tkinter import ttk , messagebox , filedialog
from ttkthemes import ThemedStyle

class LabReportEditor:
    def __init__(self, file_path):
        try:
            # Read the original LaTeX file
            with open(file_path.replace('\\', '/') , 'r', encoding='utf-8') as file:
                latex_content = file.read()
        except UnicodeDecodeError:
            # If 'utf-8' fails, try 'latin-1' or another suitable encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                latex_content = file.read()
        except Exception as e:
            file_path = file_path.replace('\\', '/')
            #print(f"Latex File not Found on {file_path}:", e)
        self.file_path = file_path
        self.old_latex_code = latex_content
        self.new_experiment_name = None
        self.experiment_no = 1 #encase its return null
        self.updated_latex_code = ""
        self.image_info_array = []
        self.latex_code_for_image = []
        self.graph_data_series = []
        self.destination_folder = None

        


    def edit_title_file(self , experiment_name ):
        title_page = self.old_latex_code[:self.old_latex_code.find("%************** End of Title Page *************") + len("%************** End of Title Page *************")]
        self.new_experiment_name = self.replace_special_characters(experiment_name)

        # Regular expression patterns for extracting information
        experiment_no_pattern = r"Experiment No\. (\d+)"
        experiment_name_pattern = r"Experiment Name: (.+?)\}"
        submission_date_pattern = r"Date of Submission : (\d{2}/\d{2}/\d{4})"
        experiment_date_pattern = r"Date of Experiment : (\d{2}/\d{2}/\d{4})"

        # Find matches using the regular expressions
        experiment_no_match = re.search(experiment_no_pattern, title_page)
        submission_date_match = re.search(submission_date_pattern, title_page)
        experiment_date_match = re.search(experiment_date_pattern, title_page)
        experiment_name_match = re.search(experiment_name_pattern, title_page)

        # Replacement
        submission_date_str = submission_date_match.group(1)
        experiment_date_str = experiment_date_match.group(1)
        submission_date = datetime.strptime(submission_date_str, '%d/%m/%Y')
        new_submission_date = submission_date + timedelta(days=7)
        new_submission_date_str = new_submission_date.strftime('%d/%m/%Y')
        self.experiment_no = int(experiment_no_match.group(1)) + 1
        old_experiment_name = experiment_name_match.group(1)

        # Perform the replacements
        updated_content = title_page.replace(f"Experiment No. {self.experiment_no-1}", f"Experiment No. {self.experiment_no}")
        updated_content = updated_content.replace(submission_date_str, new_submission_date_str)
        updated_content = updated_content.replace(experiment_date_str, submission_date_str)
        updated_content = updated_content.replace(old_experiment_name, self.new_experiment_name)
        updated_content = re.sub(old_experiment_name, self.new_experiment_name, updated_content)

        title = f"\n\\setcounter{{chapter}}{{{self.experiment_no-1}}}\n\\chapter{{Experiment Name : {self.new_experiment_name}}}"
        updated_content += f"\n\n%%%%%%%%%%%%%%% Start of Report %%%%%%%%%%%%%%%\n{title}\n"
        #print("Title page complete!!!\n")
        self.updated_latex_code += updated_content
        return self.updated_latex_code
        

    def add_image(self , image_filename, source_folder):
        try:
            # Create the destination folder if it doesn't exist
            self.destination_folder = self.file_path.replace('\\','/')
            self.destination_folder = self.destination_folder.replace(f'Experiments/Exp0{self.experiment_no-1}.tex',f'Figures/Exp0{self.experiment_no}')
            if not os.path.exists(self.destination_folder):
                os.makedirs(self.destination_folder)
            if self.destination_folder :
                dest_path = os.path.join(self.destination_folder, image_filename)

                # Copy the image from source to destination
                shutil.copy(source_folder , dest_path)

            #print(f'\n---Demo Image Added on {destination_folder}/{image_filename}\n')
        except Exception as e:
            print(f"An error occurred while adding {image_filename} image from {source_folder}: {e}")

    def image_adder(self, section):

        for image in range(len(self.image_info_array)) :
            if self.image_info_array[image][0] == section :
                img_per_row_values = self.image_info_array[image][1]
                image_path_list = self.image_info_array[image][2]

        # Validate the input values
        if img_per_row_values == 0 :
            return "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        
        # Ensure img_per_row_values is iterable
        if not isinstance(img_per_row_values, (list, tuple)):
            img_per_row_values = [img_per_row_values]
            
        if not isinstance(image_path_list, (list, tuple)):
            image_path_list = [image_path_list]

        # Initialize LaTeX code and image_path_index
        image_adder_code = ""
        image_path_index = 0


        for img_per_row in img_per_row_values :
            # Start a new figure for the row
            image_adder_code += "\\begin{figure}[h!]\n"
            image_adder_code += "    \\centering\n"

            # If there is only one image per row, don't create minipage
            if img_per_row == 1:
                # Include the image
                image_file = os.path.basename(image_path_list[image_path_index])
                self.add_image( image_file , image_path_list[image_path_index] )
                image_adder_code += f"    \\includegraphics[width=0.45\\textwidth]{{Figures/Exp0{self.experiment_no}/{image_file}}}\n"
                image_adder_code += f"    \\caption{{ {section} for Image{image_path_index} }}\n"
                #incriment
                image_path_index+=1
            else:
                # Ensure img_per_row is a positive integer
                img_per_row = max(1, int(img_per_row))
                
                # Calculate minipage width based on the number of images in the row
                minipage_width = round(1 / img_per_row - 0.05, 2)

                # Loop through each column
                for col in range(img_per_row):
                    # Start a minipage for each image
                    image_adder_code += f"    \\begin{{minipage}}{{{minipage_width}\\textwidth}}\n"
                    image_adder_code += "        \\centering\n"

                    # Include the image
                    image_file = os.path.basename(image_path_list[image_path_index])
                    self.add_image( image_file , image_path_list[image_path_index] )
                    image_adder_code += f"        \\includegraphics[width=\\textwidth]{{Figures/Exp0{self.experiment_no}/{image_file}}}\n"
                    #incriment
                    image_path_index+=1

                    # Automatically generate captions
                    image_adder_code += f"        \\caption{{ {section} for Image{image_path_index} }}\n"

                    # Close the minipage
                    image_adder_code += "    \\end{minipage}\n"

            # Close the figure for the row
            image_adder_code += "\\end{figure}\n\n"

        return image_adder_code


    def generate_graph(self, x_label , y_label ):

        # Formatting the TikZ code
        graph_code = (
            f"\\begin{{figure}}[h!]\n"
            f"    \centering\n"
            f"    \\begin{{tikzpicture}}\n"
            f"        \\begin{{axis}}[\n"
            f"            width=0.8\\textwidth,\n"
            f"            height=0.48\\textwidth,\n"
            f"            xlabel={{{x_label}}},\n"
            f"            ylabel={{{y_label}}},\n"
            f"            title={{{x_label} vs {y_label}}},\n"
            f"            grid=major,\n"
            f"        ]\n"
        )

        # Adding all data series
        for series_x_data, series_y_data, series_color in self.graph_data_series:
        # Adding data series to the TikZ code
            graph_code += f"            \\addplot[color={series_color}, mark=none] table {{\n"
            for x, y in zip(series_x_data, series_y_data):
                graph_code += f"                {x} {y}\n"
            graph_code += f"            }};\n"

        # Completing the TikZ code
        graph_code += (
            f"        \end{{axis}}\n"
            f"    \end{{tikzpicture}}\n"
            f"    \caption{{Graph Caption}}\n"
            f"    \label{{fig:graph_label}}\n"
            f"\end{{figure}}\n"
        )
        #print(graph_code)
        return graph_code
    
    def replace_special_characters(self,text):
        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }

        for char, latex_code in replacements.items():
            text = text.replace(char, latex_code)

        return text


    def process_latex_sections(self):
        # Define a regular expression pattern to match section names
        section_pattern = r"\\section\{(.*?)\}"

        # Find all matches in the LaTeX code
        sections = re.findall(section_pattern, self.old_latex_code)
        #print(sections)

        # Initialize
        updated_content = ""
        


        # Gather image information for each section
        for section in sections :
            #print(f'{section} part :\n')

            # Add section title
            updated_content += "\n\n%**********************************************\n"
            updated_content += f"\section{{{section}}}\n"

            # Handle specific sections
            if section == "Objective" or section == "Objectives":
                updated_content += "The objectives of this experiment are:\n\\begin{itemize}\n"
                for i in range(3):  # 3 objectives by default
                    updated_content += f"  \\item \n"
                updated_content += "\\end{itemize}\n"
            elif section == "Components" or section == "Required Apparatus":
                updated_content += "\n\\begin{enumerate}\n"
                for i in range(5):  # 5 components by default
                    updated_content += f"  \\item \n"
                updated_content += "\\end{enumerate}\n"
            elif section in ["Theory", "Circuit Diagram", "Experimental setup", "Result"]:
                for index  in range(len(self.latex_code_for_image)) :
                    if self.latex_code_for_image[index][0] == section :
                        image = self.latex_code_for_image[index][1]
                updated_content += image
            #print(f"{section} Added")

        self.updated_latex_code += updated_content
        ##print(self.updated_latex_code)

    def create_new_file(self):
        # Create a new file with the edited content
        new_latex_file_path = self.file_path.replace(f'Exp0{self.experiment_no-1}', f'Exp0{self.experiment_no}')

        # Check if the file already exists
        if os.path.exists(new_latex_file_path):
            # Create a backup file
            backup_path = new_latex_file_path.replace('.tex', f'_backup.tex')

            try:
                # Copy the content of the original file to the backup file
                with open(new_latex_file_path, 'r', encoding='utf-8') as original_file:
                    with open(backup_path, 'w', encoding='utf-8') as backup_file:
                        backup_file.write(original_file.read())
                #print(f"Backup created successfully! Saved on {backup_path}")

            except Exception as e:
                print(f"Error creating backup: {e}")

        try:
            with open(new_latex_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(self.updated_latex_code)

            #print(f"Edited file created successfully! Saved on {new_latex_file_path}")
            return new_latex_file_path

        except Exception as e:
            print(f"Error creating new file: {e}")

class LabReportUI_handler :
    def __init__(self , UI ):
        self.window = tk.Tk()
        self.ui = UI

        self.lab_report = None

        # Variables
        self.index = 0
        self.sections_with_image = ["Theory", "Circuit Diagram", "Experimental setup", "Result"]
        self.graph_data_series_index = 0



    def set_default_style(self, header ):
        if header != "Latex Editor":
            self.clear_window()
        style = ThemedStyle(self.window)
        style.set_theme("plastik")
        # Override specific styles
        style.configure("TLabel", font=("Helvetica", 12) , sticky=tk.W) 
        style.configure("TEntry", font=("Helvetica", 12) , sticky=tk.W) 
        style.configure("TButton", font=("Helvetica", 12) , sticky=tk.W)
        # Set the default style globally for Entry widgets
        self.window.option_add('*TEntry*Font', style.lookup("TEntry", "font"))
        self.window.option_add('*TEntry*Width', 40)
        self.window.title(header)
        self.window.geometry("800x420")
        self.window.grid_rowconfigure(0, minsize=40)
        self.window.grid_columnconfigure(0, minsize=60)
        self.window.grid_columnconfigure(4, minsize=60)
        # Title Label
        title_label = ttk.Label(self.window, text=header, font=("Helvetica", 26, "bold"))
        title_label.grid(row=1, column=1, columnspan=3, pady=10)
        self.window.grid_rowconfigure(2, minsize=50)


    def create_progressbar(self):
        #create progressbar
        self.progressbar = ttk.Progressbar(orient=tk.HORIZONTAL, length= 800)
        self.progressbar.place(x=0, y=0)

        
    def clear_window(self):
        # Clear existing elements in the main window
        for widget in self.window.winfo_children():
            if not isinstance(widget, ttk.Progressbar):
                widget.destroy()
    

    def show_success_message(self , file_path) :
        success_message = f"Lab report created successfully and saved at {file_path}"
        message = f"{success_message}\n\nDo you want to open the file now?"
        result = messagebox.askyesno("Success", message)
        # Destroy all windows and close the program
        self.window.destroy()
        if result:
            subprocess.run(["C:\Program Files\\texstudio\\texstudio.exe", file_path], check=True, shell=True)
    
    def browse_file(self , file_path_entry):
        try:
            file_path = filedialog.askopenfilename(initialdir="E:\Misc\Digital Lab Report\Experiments",filetypes=[("TeX files", "*.tex")])
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def edit_title(self , file_path_entry , experiment_name_entry ):
        try:
            file_path = file_path_entry.get()
            if not file_path:
                raise ValueError("File path is required.")
            else:
                self.lab_report = LabReportEditor(file_path)

            experiment_name = experiment_name_entry.get()
            if not experiment_name:
                raise ValueError("Experiment name is required.")
            else:
                self.lab_report.edit_title_file(experiment_name)
            
            
            # Create the additional window
            self.progressbar.step(19.99)
            self.ui.create_image_adder_window()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    

    def image_adder(self, entry, label):
        try:
            self.progressbar.step(10)
            num_images = entry.get()
            num_images_list = num_images.split()  # split the string by spaces
            num_images_int_list = []
            image_paths = []
            current_section = self.sections_with_image[self.index % 4]

            for num in num_images_list:
                num = int(num)
                num_images_int_list.append(num)

            if num_images :
                image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            while len(image_paths) != sum(num_images_int_list):
                messagebox.showwarning("Warning", f"You selected {len(image_paths)} images.You must select {sum(num_images_int_list)} images")
                image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

            self.lab_report.image_info_array.append([current_section, num_images_int_list , image_paths] )
            self.lab_report.latex_code_for_image.append( [current_section, self.lab_report.image_adder(current_section)])

            # Check the condition before incrementing the index
            if self.index == len(self.sections_with_image) - 1:
                result = messagebox.askquestion("Add Graph?", "Do you want to add a graph?")
                if result == "yes":
                    self.progressbar.step(20)

                    # Create the additional window
                    self.ui.create_graph_adder_window()
                else:
                    self.progressbar.step(40)
                    self.lab_report.process_latex_sections()
                    # Display a success message
                    self.show_success_message(self.lab_report.create_new_file())

            else:
                # Update the label text for the next section
                self.index += 1
                new_label_text = f"{self.sections_with_image[self.index % 4]} Section:"
                label.config(text=new_label_text)
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in image Adder : {str(e)}")
    

    def graph_adder(self, x_label_entry, x_data_entry, y_label_entry, y_data_entry, add_series_var , num_of_extraDataseries_entry ):
        try:
            if not x_data_entry.get() or not x_data_entry.get() :
                raise InterruptedError("X and Y data fields cannot be empty.")

            x_axis_data = [float(x) for x in (x_data_entry.get()).split()]
            y_axis_data = [float(y) for y in (y_data_entry.get()).split()]

            # Ensure x_axis_data and y_axis_data is iterable
            if not isinstance(x_axis_data, (list, tuple)):
                x_axis_data = [x_axis_data]
            if not isinstance(y_axis_data, (list, tuple)):
                y_axis_data = [y_axis_data]

            # Initialize self.graph_data_series with the first series
            self.lab_report.graph_data_series.append((x_axis_data, y_axis_data, "red"))

            self.x_axis_label = x_label_entry
            self.y_axis_label = y_label_entry

            if not add_series_var.get():
                self.progressbar.step(19.99)
                self.create_graph()
            if num_of_extraDataseries_entry :
                self.num_series = int(num_of_extraDataseries_entry)
                if self.graph_data_series_index < self.num_series:
                    self.progressbar.step(10)
                    self.ui.create_data_entry_window()
        except InterruptedError as e:
            messagebox.showerror("Error", str(e))    
                

    def create_graph(self):
        try:
            found = False
            graph = self.lab_report.generate_graph(self.x_axis_label , self.y_axis_label )

            for section in self.lab_report.latex_code_for_image:
                if section[0] == "Result":
                    section[1] += graph
                    found = True

            if not found:
                self.lab_report.latex_code_for_image.append(("Result", graph))

            self.lab_report.process_latex_sections()
            # Display a success message
            self.show_success_message(self.lab_report.create_new_file())

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in create graph : {str(e)}")
    

    def handle_data_entry(self, x_data_series_entry, y_data_series_entry):
        try:
            x_input = x_data_series_entry.get()
            if x_input:
                series_x_data = [float(x) for x in x_input.split(' ')]

            y_input = y_data_series_entry.get()
            if y_input:
                series_y_data = [float(y) for y in y_input.split(' ')]

            if not x_input or not y_input:
                raise ValueError("X and Y data fields cannot be empty.")

            series_color = ["blue", "green", "black" , "red"][self.graph_data_series_index % 4]

            self.lab_report.graph_data_series.append((series_x_data, series_y_data, series_color))

            # Clear the Entry widgets
            x_data_series_entry.delete(0, tk.END)
            y_data_series_entry.delete(0, tk.END)

            # Increment
            self.graph_data_series_index += 1
            

            if self.graph_data_series_index >= self.num_series:
                self.progressbar.step(10)
                self.create_graph()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
