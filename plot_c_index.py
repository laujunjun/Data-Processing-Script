'''
该脚本用于解析训练日志文件，并绘制 C-index 随 Epoch 变化的折线图，主要用于 生存分析模型的训练评估。
'''

import matplotlib.pyplot as plt

def parse_txt_and_plot(file_path, output_path):
    epochs = []
    train_c_index = []
    val_c_index = []

    # 读取文件并解析内容
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # 忽略空行
                parts = line.split(", ")
                epoch = int(parts[0].split(":")[1])
                train_c = float(parts[1].split(":")[1])
                val_c = float(parts[2].split(":")[1])
                
                epochs.append(epoch)
                train_c_index.append(train_c)
                val_c_index.append(val_c)

    # 绘制图表
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_c_index, label="Train C-index", color='blue')
    plt.plot(epochs, val_c_index, label="Val C-index", color='red')

    # 添加标题和标签
    plt.title("Train and Validation C-index Over Epochs", fontsize=16)
    plt.xlabel("Epoch", fontsize=14)
    plt.ylabel("C-index", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.5)

    # 保存图表到指定路径
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"图表已保存到 {output_path}")

# 指定输入文件路径和输出图片路径
file_path = "training_log.txt"  # 输入的文本文件路径
output_path = "c_index_plot.png"  # 输出图片路径
parse_txt_and_plot(file_path, output_path)
