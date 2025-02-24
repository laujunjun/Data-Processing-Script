'''
该脚本用于 对乳腺癌数据集进行分层 K 折交叉验证（Stratified K-Fold Cross-Validation），
确保不同折中 转移病例（is_metastatic_case）的比例均衡，并对训练数据进行 类别重新采样 以调整类别不均衡问题。
最终生成 包含 train、val、test 划分的 CSV 文件，用于模型训练和验证。

类别平衡处理（仅训练集）
	•	训练集中，is_metastatic（1 类）与 非转移（0 类）通常数量不均衡。
	•	重新采样 0 类样本，使其数量与 1 类样本保持 2:1 比例（可扩展支持不同比例）。
	•	重新构建 train 数据集，并保存为 CSV 文件。
'''
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import numpy as np
import os

# 加载数据
df = pd.read_csv('/9_data/chenjilong/BreastCancer/label_1253.csv')

# 将 is_metastatic 的 case_id 标记为 1，其余为 0
df['is_metastatic_case'] = df.apply(lambda x: 1 if x['label'] == 'is_metastatic' else 0, axis=1)

# 根据 case_id 对 is_metastatic_case 进行分组汇总，得到每个 case_id 是否包含 is_metastatic
case_summary = df.groupby('case_id')['is_metastatic_case'].max().reset_index()

# 使用分层 K 折交叉验证方法来平均分配 is_metastatic_case
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 为每个 case_id 分配 fold 编号
case_summary['fold'] = -1
for fold, (train_idx, test_idx) in enumerate(skf.split(case_summary, case_summary['is_metastatic_case'])):
    case_summary.loc[test_idx, 'fold'] = fold

# 将 fold 编号合并回原始数据
df = df.merge(case_summary[['case_id', 'fold']], on='case_id')

# 指定保存路径
save_path = '/9_data/ljj/PathoSig/Add_addtition_feats_10patch/label'  # 修改为您想要的路径
os.makedirs(save_path, exist_ok=True)  # 创建目录，如果目录已存在则不会创建

# 分别保存每个 fold 的数据
for fold in range(5):
    fold_df = df[df['fold'] == fold]
    test_ids = fold_df['slide_id'].unique()
    remaining_df = df[~df['slide_id'].isin(test_ids)]
    
    # 对剩余的数据按照 is_metastatic_case 进行分层抽样
    skf_remaining = StratifiedKFold(n_splits=8, shuffle=True, random_state=42)
    for _, val_idx in skf_remaining.split(remaining_df, remaining_df['is_metastatic_case']):
        val_case_ids = remaining_df.iloc[val_idx]['case_id'].unique()
        break  # 只取第一组作为验证集
    
    train_case_ids = [id_ for id_ in remaining_df['case_id'].unique() if id_ not in val_case_ids]
    
    # 根据 case_id 获取对应的 slide_id
    train_ids = remaining_df[remaining_df['case_id'].isin(train_case_ids)]['slide_id'].unique()
    val_ids = remaining_df[remaining_df['case_id'].isin(val_case_ids)]['slide_id'].unique()
    
    # 修改部分 - 重新采样，平衡 train 中的 label
    train_df = remaining_df[remaining_df['slide_id'].isin(train_ids)]
    label_1_samples = train_df[train_df['label'] == 'is_metastatic']
    label_0_samples = train_df[train_df['label'] != 'is_metastatic']
    
    # 准备不同比例的重新采样结果
    ratios = [2] #[1, 2, 3]
    for ratio in ratios:
        # 随机选择与 label_1 样本数量相等的 label_0 样本，设置随机种子
        label_0_sampled = label_0_samples.sample(n=len(label_1_samples) * ratio, random_state=42)
        
        # 合并重新采样的训练数据
        train_balanced = pd.concat([label_1_samples, label_0_sampled])
        
        # 获取重新采样后的 train 的 slide_id
        train_ids_balanced = train_balanced['slide_id'].unique()
        
        fold_data = {
            'train': train_ids_balanced,
            'val': val_ids,
            'test': test_ids
        }
        
        # 保存到 CSV 文件
        fold_df = pd.DataFrame.from_dict(fold_data, orient='index').transpose()
        fold_df.to_csv(os.path.join(save_path, f'splits_{fold}.csv'), index=False)
