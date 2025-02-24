import os
'''
该脚本的主要功能是递归删除指定目录下的所有空文件夹，并打印被删除的文件夹路径。
'''
import shutil

def delete_empty_folders(root_dir):
    """
    遍历指定目录下的所有文件夹，删除空文件夹并打印删除的文件夹路径。

    Parameters:
        root_dir (str): 要检查的根目录路径。
    """
    deleted_folders = []

    # 遍历所有子文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 如果文件夹为空（没有子文件夹且没有文件）
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)  # 删除空文件夹
                deleted_folders.append(dirpath)
            except Exception as e:
                print(f"无法删除文件夹 {dirpath}: {e}")

    # 打印结果
    if deleted_folders:
        print("已删除以下空文件夹：")
        for folder in deleted_folders:
            print(folder)
    else:
        print("没有空文件夹需要删除。")

# 示例用法
if __name__ == "__main__":
    root_directory = "/9_data/ljj/HAN_CLAM/graph_feature_10handpickedPatches_handled_missing_value/feature_1"  # 替换为实际目录路径
    delete_empty_folders(root_directory)
