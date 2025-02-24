'''
该脚本用于计算 CSV 文件中 “Coords Shape” 列的总和。
它会跳过 CSV 文件的表头，并过滤掉 包含’N/A’的行，然后将该列的数值转换为整数并进行累加，最终输出计算结果。
'''
import csv

input_file_path = 'example.csv'

coords_shape_sum = 0

with open(input_file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)  # csv.reader读取CSV文件
    
    # 跳过表头
    next(csvreader)
    
    # 遍历每一行，累加“Coords Shape”列的值
    for row in csvreader:
        # 跳过包含'N/A'的行
        if 'N/A' in row[2]:
            continue
        
        # 累加“Coords Shape”列的值
        coords_shape_sum += int(row[2])

print(f"The sum of 'Coords Shape' column is: {coords_shape_sum}")
