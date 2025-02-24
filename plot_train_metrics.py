‘’‘
该脚本用于解析训练日志文件，提取 AUC 和 C-index，并绘制 折线图 以便 评估模型训练过程。

格式：
  Epoch: 1, Train AUC: 0.85, Val AUC: 0.83, Train C-index: 0.75, Val C-index: 0.72
  Epoch: 2, Train AUC: 0.87, Val AUC: 0.85, Train C-index: 0.78, Val C-index: 0.74
’‘’
import re
import matplotlib.pyplot as plt

def parse_log(file_path):
    epochs, train_auc, val_auc, train_c_index, val_c_index = [], [], [], [], []
    
    # 打开并解析文件
    with open(file_path, 'r') as f:
        for line in f:
            # 使用正则表达式提取数值
            match = re.match(r"Epoch:\s*(\d+),\s*Train AUC:\s*([\d.]+),\s*Val AUC:\s*([\d.]+),\s*Train C-index:\s*([\d.]+),\s*Val C-index:\s*([\d.]+)", line)
            if match:
                epochs.append(int(match.group(1)))
                train_auc.append(float(match.group(2)))
                val_auc.append(float(match.group(3)))
                train_c_index.append(float(match.group(4)))
                val_c_index.append(float(match.group(5)))
    
    return epochs, train_auc, val_auc, train_c_index, val_c_index

def plot_metrics(epochs, train_auc, val_auc, train_c_index, val_c_index):
    plt.figure(figsize=(12, 6))

    # 绘制 AUC 曲线
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_auc, label='Train AUC', color='blue')
    plt.plot(epochs, val_auc, label='Val AUC', color='orange')
    plt.xlabel('Epoch')
    plt.ylabel('AUC')
    plt.title('Train and Validation AUC')
    plt.legend()

    # 绘制 C-index 曲线
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_c_index, label='Train C-index', color='green')
    plt.plot(epochs, val_c_index, label='Val C-index', color='red')
    plt.xlabel('Epoch')
    plt.ylabel('C-index')
    plt.title('Train and Validation C-index')
    plt.legend()

    plt.tight_layout()
    
    # 保存图像为文件
    plt.savefig('train_val.png')  # 保存到当前目录
    plt.show()

if __name__ == '__main__':
    # 文件路径
    file_path = 'training_log.txt'
    
    # 解析文件并绘制图像
    epochs, train_auc, val_auc, train_c_index, val_c_index = parse_log(file_path)
    plot_metrics(epochs, train_auc, val_auc, train_c_index, val_c_index)
