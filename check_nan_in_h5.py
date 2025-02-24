'''
这个脚本用于 检查 HDF5 (.h5) 文件中的 features 数据集是否包含 NaN 值。
它会遍历指定目录及其所有子目录，逐个检查 .h5 文件，判断 features 数据集中是否存在 NaN，
并输出包含 NaN 的文件路径和具体索引位置。如果文件中未找到 features 数据集，则会发出警告。
'''
import os
import h5py
import numpy as np

def check_nan_in_h5_files(directory):
    # 遍历目录及其子目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                with h5py.File(file_path, 'r') as h5_file:
                    if 'features' in h5_file:
                        features = h5_file['features'][:]
                        if np.isnan(features).any():
                            nan_indices = np.argwhere(np.isnan(features))
                            print(f"NaN values found in file: {file_path}")
                            print(f"NaN indices: {nan_indices}")
                    else:
                        print(f"'features' dataset not found in file: {file_path}")

if __name__ == "__main__":
    directory = '/path/to/nan_debug'  # 替换为你的目录路径
    check_nan_in_h5_files(directory)
