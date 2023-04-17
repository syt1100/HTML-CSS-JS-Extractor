pyinstaller --onefile --windowed --name="HTML分离工具" html_splitter_v2.py


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / 'input'
    output_dir = base_dir / 'output'

    # 获取用户输入的文件名
    file_name = input("请输入要处理的HTML文件名（不包含扩展名）：")

    # 使用用户输入的文件名构建文件路径
    input_file = input_dir / f"{file_name}.html"

    html_content = read_file(input_file)
    css_content = extract_css(html_content)
    js_content = extract_js(html_content)
    new_html_content = extract_html(html_content)

    # 在输出文件夹中为每个输入文件创建一个单独的文件夹
    output_subdir = output_dir / file_name
    output_subdir.mkdir(parents=True, exist_ok=True)

    # 根据用户输入的文件名保存文件
    write_file(output_subdir / f"{file_name}.css", css_content)
    write_file(output_subdir / f"{file_name}.js", js_content)
    write_file(output_subdir / f"{file_name}.html", new_html_content)

    print("CSS文件保存成功")
    print("JS文件保存成功")
    print("HTML文件保存成功")
    print("CSS文件保存成功")
    print("JS文件保存成功")
    print("HTML文件保存成功")
