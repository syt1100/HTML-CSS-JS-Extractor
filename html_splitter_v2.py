import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_css(html_str):
    css_regex = re.compile(r'<style>[\s\S]*<\/style>')
    css_content = css_regex.search(html_str)
    if css_content:
        return css_content.group(0).replace('<style>', '').replace('</style>', '')
    return ''

def extract_js(html_str):
    js_regex = re.compile(r'<script>[\s\S]*<\/script>')
    js_content = js_regex.search(html_str)
    if js_content:
        return js_content.group(0).replace('<script>', '').replace('</script>', '')
    return ''

def extract_html(html_str):
    css_regex = re.compile(r'<style>[\s\S]*<\/style>')
    js_regex = re.compile(r'<script>[\s\S]*<\/script>')
    return css_regex.sub('<link rel="stylesheet" href="./index.css"/>', js_regex.sub('<script type="text/javascript" src="./index.js"></script>', html_str))

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def process_file():
    process_status_label.config(text="正在处理...")  # 显示“正在处理...”
    app.update()  # 更新GUI显示

    input_file = Path(input_file_entry.get())
    file_name = input_file.stem

    # 使用输入文件所在的文件夹作为输出文件夹
    output_dir = input_file.parent
    output_subdir = output_dir / file_name

    # 检查同名文件夹是否存在
    if output_subdir.exists():
        overwrite = messagebox.askyesno(title="覆盖文件夹？", message=f"文件夹 {output_subdir} 已存在，是否覆盖？")
        if not overwrite:
            process_status_label.config(text="")  # 清除“正在处理...”提示
            result_label.config(text="处理失败")  # 更新结果标签为“处理失败”
            return

    output_subdir.mkdir(parents=True, exist_ok=True)

    html_content = read_file(input_file)
    css_content = extract_css(html_content)
    js_content = extract_js(html_content)
    new_html_content = extract_html(html_content)

    write_file(output_subdir / f"{file_name}.css", css_content)
    write_file(output_subdir / f"{file_name}.js", js_content)
    write_file(output_subdir / f"{file_name}.html", new_html_content)

    process_status_label.config(text="")  # 清除“正在处理...”提示
    result_label.config(text="处理完成")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / 'output'

    app = tk.Tk()
    app.title("HTML分离工具")

    input_file_label = tk.Label(app, text="输入文件：")
    input_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    input_file_entry = tk.Entry(app, width=50)
    input_file_entry.grid(row=0, column=1, padx=10, pady=10)

    browse_button = tk.Button(app, text="浏览", command=browse_input_file)
    browse_button.grid(row=0, column=2, padx=10, pady=10)

    process_button = tk.Button(app, text="处理文件", command=process_file)
    process_button.grid(row=1, column=1, padx=10, pady=10)

    result_label = tk.Label(app, text="")
    result_label.grid(row=2, column=1, padx=10, pady=10)

    process_status_label = tk.Label(app, text="")
    process_status_label.grid(row=3, column=1, padx=10, pady=10)

    app.mainloop()