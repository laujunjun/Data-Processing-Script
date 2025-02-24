'''
该脚本用于 遍历指定目录中的所有 CSV 文件，并填充缺失值，
主要作用是对目录下的所有 CSV 文件进行数据填充，用 200 替换 NaN（缺失值）。
'''

import os
import pandas as pd

# 定义根目录
root_dir = '/9_data/ljj/HoverNet_feature/feature_multi/feature_0'

# 定义需要填充的值
fill_value = 200

# 遍历根目录下的所有文件和文件夹
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.csv'):
            # 获取文件完整路径
            file_path = os.path.join(root, file)
            
            # 读取CSV文件，空值用空字符串表示
            df = pd.read_csv(file_path, na_values=['', ' ', ','])
            
            # 填充NaN值
            df.fillna(fill_value, inplace=True)
            
            # 直接保存到原始文件
            df.to_csv(file_path, index=False)
            print(f'Processed {file_path}')

print("All files have been processed.")
