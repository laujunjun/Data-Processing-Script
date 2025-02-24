'''
该脚本用于加载并检查 HDF5 (.h5) 文件的结构和数据完整性。
它遍历 HDF5 文件的所有数据集和分组，打印数据集的形状和数据类型，并检查数据集中是否存在非法值（NaN 或 Inf）。
此外，脚本还检测某些关键数据集（如 coords 和 feat）的行数是否异常（N=0 或 N=1），并发出警告。
'''

import h5py
import numpy as np

file_path = "example.h5"

def check_invalid_values(dataset_name, data):
    """检查数据集中是否有非法值（NaN 或 Inf）"""
    if not isinstance(data, np.ndarray):
        return
    has_nan = np.isnan(data).any()
    has_inf = np.isinf(data).any()
    if has_nan or has_inf:
        print(f"Invalid values found in dataset '{dataset_name}': NaN={has_nan}, Inf={has_inf}")
    # else:
        # print(f"No invalid values found in dataset '{dataset_name}'.")

def print_h5_structure(name, obj):
    """打印文件结构并检查非法值与形状"""
    if isinstance(obj, h5py.Group):
        print(f"Group: {name}")
    elif isinstance(obj, h5py.Dataset):
        print(f"Dataset: {name}, Shape: {obj.shape}, Dtype: {obj.dtype}")
    if isinstance(obj, h5py.Dataset):  # 只处理数据集        
        # 检查数据集形状
        try:
            if "coords" in name or "feat" in name:
                data = obj[()]  # 加载整个数据集
                if obj.shape[0] == 1:
                    print(f"WARNING: Dataset '{name}' has N=1.")
                elif obj.shape[0] == 0:
                    print(f"WARNING: Dataset '{name}' has N=0.")
                check_invalid_values(name, data)
        except Exception as e:
            print(f"Error reading dataset '{name}': {e}")

# 打开 HDF5 文件并遍历结构
with h5py.File(file_path, "r") as h5file:
    h5file.visititems(print_h5_structure)
