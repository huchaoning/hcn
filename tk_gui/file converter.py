import tkinter as tk
from tkinter import filedialog

import numpy as np
from pathlib import Path
import os 
import pandas as pd
from PIL import Image

def read_single(file):
    if os.path.exists(file):
        extension = (Path(file).suffix).lower()[1:]
    else:
        return
    
    if extension == 'npy':
        return np.load(file)
    
    if extension in ('tif', 'tiff', 'bmp'):
        img = Image.open(file)
        array = []
        for i in range(img.n_frames):
            img.seek(i)
            array.append(np.array(img))
        array = np.array(array)
        if np.shape(array)[0] == 1:
            return array[0]
        else:
            return array
    
    if extension == 'csv':
        return np.array(pd.read_csv(file, header=None))
    

def read(file_list):
    return {file: read_single(file) for file in file_list}


def save(data_dic, extension, root_path):
    extension = extension[1:].lower()
    for k, v in data_dic.items():
        name = f'{Path(k).stem}.{extension}'
        path = os.path.join(root_path, name)

        if extension == 'npy':
            np.save(path, v)

        if extension == 'csv':
            pd.DataFrame(v).to_csv(path, header=None, index=None)


class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Converter')
        self.file_paths = []
        self.converted_files = []
        # Dictionary with file extension and their display names
        self.file_types = {
            '.csv': 'CSV files (.csv)',
            '.npy': 'Numpy files (.npy)',
            '.tif': 'TIFF files (.tif)'
        }
        # Reverse mapping for converting file types back to extensions
        self.label_to_extension = {label: ext for ext, label in self.file_types.items()}
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.create_select_button()
        self.create_listboxes()
        self.create_conversion_button()
        self.create_dropdown()
        self.create_save_button()

    def create_select_button(self):
        self.select_button = tk.Button(self.main_frame, text='Select Files', command=self.select_files)
        self.select_button.grid(row=0, column=0, padx=10, pady=5)

    def create_listboxes(self):
        self.left_listbox = self.create_listbox(row=1, column=0)
        self.right_listbox = self.create_listbox(row=1, column=2)

    def create_conversion_button(self):
        self.convert_button = tk.Button(self.main_frame, text='->', command=self.convert_files)
        self.convert_button.grid(row=1, column=1, padx=10, pady=10)

    def create_dropdown(self):
        self.converted_file_type_var = tk.StringVar(value='Convert to...')
        # Create a dropdown menu with labels including file extensions
        self.dropdown_menu = tk.OptionMenu(self.main_frame, self.converted_file_type_var, *self.file_types.values())
        self.dropdown_menu.grid(row=0, column=2, padx=10, pady=5)

    def create_save_button(self):
        self.save_button = tk.Button(self.main_frame, text='Save', command=self.save_files)
        self.save_button.grid(row=2, column=2, pady=10)

    def create_listbox(self, row, column):
        listbox = tk.Listbox(self.main_frame, width=20, height=15, exportselection=0, selectmode=tk.NONE)
        listbox.grid(row=row, column=column, padx=10, pady=10)
        return listbox

    def select_files(self):
        file_types = [('AVI files', '*.avi'), ('Numpy files', '*.npy'), ('CSV files', '*.csv'),
                      ('TIFF files', '*.tif'), ('Bitmap files', '*.bmp')]
        file_paths = filedialog.askopenfilenames(
            title='Select Files',
            initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'),
            filetypes=file_types
        )
        self.file_paths = list(file_paths)
        self.update_listboxes()

    def update_listboxes(self):
        self.update_listbox(self.left_listbox, self.file_paths)
        self.update_listbox(self.right_listbox, self.converted_files)

    def update_listbox(self, listbox, files):
        listbox.delete(0, tk.END)
        if files:
            for file_path in files:
                listbox.insert(tk.END, os.path.basename(file_path))
        else:
            listbox.insert(tk.END, 'No files')

    def convert_files(self):
        selected_label = self.converted_file_type_var.get()
        file_extension = self.label_to_extension.get(selected_label)
        
        if not file_extension:
            return

        self.works = read(self.file_paths)

        self.converted_files = [self.convert_file_extension(file_path, file_extension) for file_path in self.file_paths]
        self.update_listboxes()

    def convert_file_extension(self, file_path, new_extension):
        base_name, _ = os.path.splitext(file_path)
        return base_name + new_extension

    def save_files(self):
        save_directory = filedialog.askdirectory(
            title='Select Directory to Save Files',
            initialdir=os.path.join(os.path.expanduser('~'), 'Desktop')
        )
        if save_directory:
            
            selected_label = self.converted_file_type_var.get()
            file_extension = self.label_to_extension.get(selected_label)

            save(self.works, file_extension, save_directory)
        else:
            print('No directory selected for saving files.')

if __name__ == '__main__':
    root = tk.Tk()
    app = FileConverterApp(root)
    root.resizable(False, False)
    root.mainloop()
