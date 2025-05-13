import os
from PyPDF2 import PdfReader  # 请确保已安装 PyPDF2 库：pip install PyPDF2


def extract_text_from_single_pdf(pdf_filepath):
    """
    Extracts text from a single PDF file.
    Args:
        pdf_filepath (str): The path to the PDF file.
    Returns:
        str: The extracted text, or None if an error occurred.
    """
    text = ""
    try:
        with open(pdf_filepath, "rb") as file:
            reader = PdfReader(file)
            if reader.is_encrypted:
                try:
                    reader.decrypt("")  # Attempt to decrypt with an empty password
                except Exception as e:
                    print(f"无法解密受密码保护的 PDF 文件 {pdf_filepath}: {e}")
                    return None

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += (
                        page_text + "\n"
                    )  # Add a newline after each page's text for better readability
        return text
    except FileNotFoundError:
        print(f"错误：文件未找到 {pdf_filepath}")
        return None
    except Exception as e:
        print(f"读取 PDF 文件 {pdf_filepath} 时出错: {e}")
        return None


def convert_pdfs_in_directory_to_txt(source_directory, output_directory):
    """
    Finds all PDF files in the specified source directory, extracts their text,
    and saves it to .txt files with the same base name in the output_directory.
    Args:
        source_directory (str): The path to the directory containing PDF files.
        output_directory (str): The path to the directory where TXT files will be saved.
    """
    found_pdfs = False
    if not os.path.isdir(source_directory):
        print(f"错误：源目录 {source_directory} 不存在或不是一个目录。")
        return

    # Ensure the output directory exists, create it if it doesn't
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.lower().endswith(".pdf"):
            found_pdfs = True
            pdf_filepath = os.path.join(source_directory, filename)
            print(f"正在处理 {pdf_filepath}...")

            extracted_text = extract_text_from_single_pdf(pdf_filepath)

            if (
                extracted_text is not None and extracted_text.strip()
            ):  # Ensure extracted text is not empty
                base_filename = os.path.splitext(filename)[0]
                txt_filename = base_filename + ".txt"
                txt_filepath = os.path.join(output_directory, txt_filename)

                try:
                    with open(txt_filepath, "w", encoding="utf-8") as txt_file:
                        txt_file.write(extracted_text)
                    print(f"成功将 {filename} 转换为 {txt_filepath}")
                except Exception as e:
                    print(f"写入 TXT 文件 {txt_filepath} 时出错: {e}")
            elif extracted_text is None:
                print(f"由于提取错误，已跳过为 {filename} 创建 TXT 文件。")
            else:  # extracted_text is empty or whitespace
                print(f"从 {filename} 中未提取到文本内容，已跳过创建 TXT 文件。")

    if not found_pdfs:
        print(f"在目录 {source_directory} 中未找到 PDF 文件。")


if __name__ == "__main__":
    # --- 用户配置区域 ---
    # 请在此处指定您的 PDF 源文件夹路径和 TXT 目标文件夹路径
    # 示例:
    # source_pdf_directory = r"C:\Users\YourUser\Documents\PDF_Presentations"
    # target_txt_directory = r"C:\Users\YourUser\Documents\TXT_Outputs"

    # 默认情况下，脚本会查找其所在目录下的 "pdf_files" 文件夹作为源，
    # 并在其所在目录下创建 "txt_files" 文件夹作为输出。
    script_base_directory = os.path.dirname(os.path.abspath(__file__))

    source_pdf_directory = os.path.join(
        script_base_directory, "PPT_OCR_2025"
    )  # PDF 源文件夹
    target_txt_directory = os.path.join(
        script_base_directory, "TXT2025"
    )  # TXT 输出文件夹

    # --- 配置结束 ---

    # 确保源目录存在，如果不存在则提示用户创建
    if not os.path.isdir(source_pdf_directory):
        print(f"提示：默认 PDF 源目录 {os.path.abspath(source_pdf_directory)} 不存在。")
        print(
            f"请在该位置创建文件夹并放入 PDF 文件，或修改脚本中的 'source_pdf_directory' 变量。"
        )
    else:
        print(f"开始在目录中进行 PDF 到 TXT 的转换:")
        print(f"源 PDF 目录: {os.path.abspath(source_pdf_directory)}")
        print(f"目标 TXT 目录: {os.path.abspath(target_txt_directory)}")
        convert_pdfs_in_directory_to_txt(source_pdf_directory, target_txt_directory)
        print("转换过程已完成。")
