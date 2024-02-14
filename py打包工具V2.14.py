import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import os
import sys
import subprocess
import shutil
import glob


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(
            "py打包工具V2.14 (python环境,pyinstaller模块开发）")  # 命令符：pip install pyinstaller   tkinter模块 pip install tkinter

        self.geometry("450x590")

        # 选择主程序文件按钮
        self.file_label = tk.Label(self, text="选择主程序py文件：")
        self.file_label.pack()
        self.file_button = tk.Button(self, text="点击浏览", command=self.select_file, width=20)
        self.file_button.pack()

        # 选择图标文件按钮
        self.icon_label = tk.Label(self, text="选择图标 ico（可选）：")
        self.icon_label.pack()
        self.icon_button = tk.Button(self, text="点击浏览", command=self.select_icon, width=20)
        self.icon_button.pack()

        # 选择输出目录按钮
        self.output_label = tk.Label(self, text="选择输出目录（可选）：")
        self.output_label.pack()
        self.output_button = tk.Button(self, text="点击浏览", command=self.select_output_directory, width=20)
        self.output_button.pack()

        # 指定依赖路径输入框
        if getattr(sys, 'frozen', False):
            self.dep_label = tk.Label(self, text="指定含依赖路径(tk,tcl,tcl8)：")
            self.dep_label.pack()
            self.dep_entry = tk.Entry(self)
            self.dep_entry.pack()
            self.dep_entry.insert(0, os.getcwd())

        # 更改软件名称输入框
        self.name_label = tk.Label(self, text="更改软件名称（可选）：")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        # 选择打包类型
        self.type_label = tk.Label(self, text="请选择打包类型：")  # 备注：需要生成软件打包母exe程序时，需要打包目录；再用打包母exe程序打包其他代码
        self.type_label.pack()
        self.type_var = tk.StringVar()
        self.type_var.set("单文件(-onefile)")
        self.type_radio1 = tk.Radiobutton(self, text="单文件(-onefile)", variable=self.type_var, value="单文件(-onefile)")
        self.type_radio1.pack()
        self.type_radio2 = tk.Radiobutton(self, text="目   录(-onedir)", variable=self.type_var,
                                          value="目  录(-onedir)")
        self.type_radio2.pack()

        # 控制台窗口选择
        self.console_label = tk.Label(self, text="控制台窗口（命令符）：")
        self.console_label.pack()
        self.console_var = tk.BooleanVar()
        self.console_var.set(False)
        self.console_check = tk.Checkbutton(self, text="打开/关闭（窗口）", variable=self.console_var)
        self.console_check.pack()

        # 生成可执行文件按钮
        self.generate_button = tk.Button(self, text="生成可执行文件（点击）", command=self.generate_executable, width=50)
        self.generate_button.pack(pady=10)
        self.generate_button.pack()

        # 生成过程显示框
        self.process_text = tk.Text(self, height=10, width=50)
        self.process_text.pack()

        # 进度条
        self.progress = Progressbar(self, orient=tk.HORIZONTAL, length=355, mode='determinate')
        self.progress.pack()

        # Variables to store selected paths
        self.file_path = None
        self.icon_path = None
        self.output_directory = None

        self.process_text.insert(tk.END, "备注说明： \n")
        self.process_text.insert(tk.END, "1. python环境2.7以上,pyinstaller模块开发；给初学者提供支持！ \n")
        self.process_text.insert(tk.END, "2. pyinstaller模块--命令符输入： pip install pyinstaller \n")
        self.process_text.insert(tk.END, "3. tkinter模块--命令符输入： pip install tkinter \n")
        self.process_text.insert(tk.END, "4. 用打包工具程序打包别的py代码时，注意要有依赖：tk tcl tcl8  三个文件包；默认已在打包程序目录里了，可复制文件包路径到填写路径栏里 \n")
        self.process_text.insert(tk.END, "5. 如用代码运行打包其他代码时，无限制；如需把自身打包生成软件，即打包母exe程序时，需要把自身打包成目录文件夹包；再运行打包母exe"
                                         "程序打包其他代码 \n")
        self.process_text.insert(tk.END, "...... \n")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        self.file_label.config(text="选择主程序文件：" + file_path)
        self.file_path = file_path

    def select_icon(self):
        icon_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        self.icon_label.config(text="选择图标文件（可选）：" + icon_path)
        self.icon_path = icon_path

    def select_output_directory(self):
        output_directory = filedialog.askdirectory()
        self.output_label.config(text="选择输出目录（可选）：" + output_directory)
        self.output_directory = output_directory

    def update_progress(self, value=0):
        self.progress['value'] = value
        self.progress.update()
        self.progress.update_idletasks()  # 更新进度条显示

    def generate_executable(self):
        file_path = self.file_path
        if not file_path:
            self.process_text.insert(tk.END, "请选择主程序文件！")
            return

        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)

        os.chdir(file_dir)

        command = ['pyinstaller', '--onefile']

        icon_path = self.icon_path
        if icon_path:
            command.extend(['--icon', icon_path])

        output_directory = self.output_directory
        if not output_directory:
            output_directory = file_dir  # Use the original directory if not selected

        name = self.name_entry.get()
        if self.type_var.get() == "单文件(-onefile)":
            output_directory = os.path.join(output_directory, name if name else file_name[:-3])
            if not os.path.exists(output_directory):
                os.makedirs(output_directory, exist_ok=True)

            if getattr(sys, 'frozen', False):
                command.extend(['--add-data', f"{os.path.join(self.dep_entry.get(), 'tcl')};tcl"])
                command.extend(['--add-data', f"{os.path.join(self.dep_entry.get(), 'tcl8')};tcl8"])
                command.extend(['--add-data', f"{os.path.join(self.dep_entry.get(), 'tk')};tk"])

        command.extend(['--distpath', output_directory])
        if name:
            command.extend(['--name', name])

        package_type = self.type_var.get()
        if package_type == "目  录(-onedir)":
            command.append('--onedir')

        console = self.console_var.get()
        if not console:
            command.append('--noconsole')

        command.append(file_name)

        self.process_text.insert(tk.END, "开始生成可执行文件...\n")
        self.process_text.update()

        # 创建临时文件用于存储生成过程的输出
        temp_file = "temp_output.txt"
        with open(temp_file, "w") as f:
            # 将标准输出和标准错误重定向到临时文件
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            total_lines = 0
            for line in process.stdout:
                # line = line.decode('utf-8')
                self.process_text.insert(tk.END, line)
                self.process_text.see(tk.END)  # 滚动显示最新的输出
                total_lines += 1
                progress_value = int((total_lines / 100) * 100)  # 计算进度条的值
                self.update_progress(progress_value)

        # 等待子进程完成，并确保文件被关闭
        process.communicate()
        # 删除临时文件
        os.remove(temp_file)

        # 删除build文件夹
        build_dir = os.path.join(file_dir, "build")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        # 指定缓存目录
        cache_directory = file_dir
        # 定义spec文件扩展名
        spec_extension = '.spec'
        # 查找并删除缓存目录下的所有spec文件
        for spec_file in glob.glob(os.path.join(cache_directory, '*' + spec_extension)):
            os.remove(spec_file)
            print(f'Removed cached spec file: {spec_file}')

        if package_type == "目  录(-onedir)" and getattr(sys, 'frozen', False):
            output_directory = os.path.join(output_directory, name if name else file_name[:-3])
            copy_status = self.copy_tcl_and_tk_folders(os.path.join(os.getcwd()), output_directory)
            self.process_text.insert(tk.END, "恭喜！生成完成！\n" if copy_status else "很遗憾，生成失败！")
            self.update_progress(100)
            return
        self.process_text.insert(tk.END, "分享者QQ:790544312！\n")
        self.process_text.insert(tk.END, "恭喜！生成完成！\n")
        self.update_progress(100)

    def copy_tcl_and_tk_folders(self, current_working_dir, target_folder_name):
        target_parent_folder = os.path.join(current_working_dir, target_folder_name)

        # 确保目标父目录存在，如果不存在则创建
        if not os.path.exists(target_parent_folder):
            os.makedirs(target_parent_folder)

        copied_folders = []
        for root, dirs, files in os.walk(current_working_dir):
            for folder_name in ['tcl', 'tcl8', 'tk']:
                matched_folder = next((d for d in dirs if d.startswith(folder_name)), None)

                if matched_folder:
                    source_folder = os.path.join(root, matched_folder)
                    target_folder = os.path.join(target_parent_folder, matched_folder)

                    # 检查源文件夹是否存在且为目标类型
                    if os.path.exists(source_folder) and os.path.isdir(source_folder):
                        # 如果目标文件夹不存在或不为空，则执行复制操作
                        if not os.path.exists(target_folder) or not os.listdir(target_folder):
                            try:
                                shutil.copytree(source_folder, target_folder)
                                copied_folders.append(matched_folder)
                                self.process_text.insert(tk.END, f"成功复制 {matched_folder} 文件夹到新的文件夹中！\n")
                            except Exception as e:
                                self.process_text.insert(tk.END, f"复制 {matched_folder} 过程中发生错误: {str(e)} \n")
                                return False

        return True


app = Application()
app.mainloop()
