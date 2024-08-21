import os
import json

#设定当前目录，可以根据当前目录找寻目标目录下的目标文件
# def read_json_file(start_dir, target_folder, target_file):
#     for root, dirs, files in os.walk(start_dir):
#         if target_folder in dirs:
#             folder_path = os.path.join(root, target_folder)
#             json_file_path = os.path.join(folder_path, target_file)
#             if os.path.exists(json_file_path):
#                 try:
#                     with open(json_file_path, 'r', encoding='utf-8') as file:
#                         data = json.load(file)
#                     return data
#                 except json.JSONDecodeError:
#                     print(f"错误：文件 '{json_file_path}' 不是有效的JSON格式。")
#                     return None
#     print(f"错误：未找到文件夹 '{target_folder}' 或文件 '{target_file}'。")
#     return None

def read_json_file(target_folder, target_file):
    json_file_path = os.path.join(target_folder, target_file)
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            print(f"错误：文件 '{json_file_path}' 不是有效的JSON格式。")
            return None
    print(f"错误：未找到文件夹 '{target_folder}' 或文件 '{target_file}'。")
    return None