import tkinter as tk
from tkinter import filedialog
import os

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File selector')
        self.create_widgets()
        self.file_paths = []  # 内存中保存文件路径的列表

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text='')
        self.info_label.pack(pady=10)

        # 创建选择文件的按钮
        self.select_button = tk.Button(self.root, text="选择文件", command=self.select_files)
        self.select_button.pack(pady=10)

        # 创建显示文件的Listbox
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=30, height=15, exportselection=0)
        self.file_listbox.pack(pady=10)

        # 创建上移、下移、删除和确认按钮
        self.move_up_button = tk.Button(self.root, text="上移", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.move_down_button = tk.Button(self.root, text="下移", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.root, text="删除", command=self.delete_file)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.confirm_button = tk.Button(self.root, text="确认", command=self.confirm_selection)
        self.confirm_button.pack(side=tk.LEFT, padx=5, pady=5)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(title="选择文件", filetypes=[("所有文件", "*.*")])
        self.file_paths = list(file_paths)  # 保存文件路径到内存中
        self.update_listbox()

    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)  # 清空现有列表
        for file_path in self.file_paths:
            # 提取文件名并显示
            file_name = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, file_name)

    def move_up(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:
                # 交换路径
                self.file_paths[index], self.file_paths[index - 1] = self.file_paths[index - 1], self.file_paths[index]
                self.update_listbox()
                self.file_listbox.select_set(index - 1)  # 重新选择移动后的项

    def move_down(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.file_paths) - 1:
                # 交换路径
                self.file_paths[index], self.file_paths[index + 1] = self.file_paths[index + 1], self.file_paths[index]
                self.update_listbox()
                self.file_listbox.select_set(index + 1)  # 重新选择移动后的项

    def delete_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            # 从内存中的列表中删除文件
            del self.file_paths[index]
            # 更新Listbox
            self.update_listbox()
            # 清除选择
            self.file_listbox.selection_clear(0, tk.END)

    def confirm_selection(self):
        # 打印当前选择的文件路径
        print("选择的文件路径数组:")
        for path in self.file_paths:
            print(path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    # scale = 1
    # root.geometry(f'{int(640*scale)}x{int(360*scale)}')
    root.resizable(False, False)
    root.mainloop()
