'''
该脚本用于为不同数据集（train、val、test）匹配标签，并生成新的 CSV 文件。
它从两个 CSV 文件中读取 样本名称 和 标签信息，然后根据样本名称查找对应的标签，
并输出新的 CSV 文件，最终用于后续模型训练或分析。
'''

import pandas as pd

# 读取样本名称的CSV文件
samples_df = pd.read_csv('data.csv')

# 读取包含label的CSV文件
label_df = pd.read_csv('/label.csv')

# 将label列中的值转换为0或1
label_df['label'] = label_df['label'].apply(lambda x: 0 if x == 'no_metastatic' else 1)

# 创建一个字典用于快速查找label
label_dict = dict(zip(label_df['slide_id'], label_df['label']))

# 函数：根据样本名获取label
def get_label(slide_id):
    return label_dict.get(slide_id, None)

output_dir = '/9_data/ljj/PathoSig/Add_addtition_feats_10patch/label/2_to_1/'

# 为每种数据集创建新的DataFrame
for dataset in ['train', 'val', 'test']:
    # 获取当前数据集的样本名
    slides = samples_df[dataset].dropna()
    
    # 创建新的DataFrame，包含slide_id和label
    new_df = pd.DataFrame({
        'slide_id': slides,
        'label': slides.apply(get_label)
    })
    
    # 将新的DataFrame保存为CSV文件
    new_df.to_csv(f'{output_dir}fold4_{dataset}.csv', index=False)

print("CSV文件生成完成。")
