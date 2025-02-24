'''
该脚本用于加载并检查 .pt 文件的数据内容，
支持 PyTorch 保存的 dict 或 torch.Tensor 类型的数据。
它能够打印数据的基本信息，如类型、形状、部分内容，并检查数据中是否存在 NaN 或 Inf 等非法值。
'''

import torch

# 指定 .pt 文件路径
pt_file_path = 'example.pt'

# 加载 .pt 文件
loaded_data = torch.load(pt_file_path)

# 打印文件内容类型
print(f"Loaded data type: {type(loaded_data)}")

# 检查数据中是否存在非法值
def check_invalid_values(key, tensor):
    if not isinstance(tensor, torch.Tensor):
        return
    has_nan = torch.isnan(tensor).any().item()
    has_inf = torch.isinf(tensor).any().item()
    # if has_nan or has_inf:
    #     print(f"Invalid values found! NaN: {has_nan}, Inf: {has_inf}")
    # else:
    #     print("No invalid values found in this tensor.")
    if has_nan or has_inf:
        print(f"Invalid values found!{key} NaN: {has_nan}, Inf: {has_inf}")


# 如果保存的是字典，遍历键值对
if isinstance(loaded_data, dict):
    for key, value in loaded_data.items():
        print(f"Key: {key}")
        if isinstance(value, torch.Tensor):
            print(f"Value shape: {value.shape}")
            print(f"Value sample: {value.flatten()[:10]}")  # 打印前10个元素的值
            check_invalid_values(key, value)
        # else:
            # print(f"Value type: {type(value)}")
            # print(f"Value content: {value}")

# 如果保存的是张量，直接查看形状和部分内容
elif isinstance(loaded_data, torch.Tensor):
    print(f"Tensor shape: {loaded_data.shape}")
    print(f"Tensor sample: {loaded_data.flatten()[:10]}")  # 打印前10个元素的值
    check_invalid_values(loaded_data)

# 如果类型未知，提醒用户
else:
    print("Unknown data type. Please inspect manually.")
