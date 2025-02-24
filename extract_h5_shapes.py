'''
该脚本用于 提取并记录 h5 文件中的特征形状信息，遍历 h5_files 目录中的所有 .h5 文件，
读取 features 和 coords 数据集的形状，并将结果保存到 CSV 文件 shape_of_feature.csv 中。
'''

import os
import h5py
import csv

# 定义h5_files文件夹路径
h5_files_folder = 'h5_files'
output_file_path = 'shape_of_feature.csv'

# 打开输出文件
with open(output_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # 写入CSV文件的表头
    csvwriter.writerow(['WSI Name', 'Features Shape', 'Coords Shape'])

    # 遍历h5_files文件夹中的每个.h5文件
    for h5_file_name in os.listdir(h5_files_folder):
        h5_file_path = os.path.join(h5_files_folder, h5_file_name)
        
        # 检查文件是否为.h5文件
        if not h5_file_name.endswith('.h5'):
            continue
        
        # 去掉文件名中的.h5后缀
        wsi_name = os.path.splitext(h5_file_name)[0]
        
        # 打开h5文件并输出features数据集和coords数据集的形状
        with h5py.File(h5_file_path, 'r') as h5_file:
            if 'features' in h5_file and 'coords' in h5_file:
                features_shape = h5_file['features'].shape[1]
                coords_shape = h5_file['coords'].shape[0]
                csvwriter.writerow([wsi_name, features_shape, coords_shape])
            else:
                missing_datasets = []
                if 'features' not in h5_file:
                    missing_datasets.append('features dataset not found')
                if 'coords' not in h5_file:
                    missing_datasets.append('coords dataset not found')
                csvwriter.writerow([wsi_name, '; '.join(missing_datasets), 'N/A'])

print(f"Results have been written to {output_file_path}")
