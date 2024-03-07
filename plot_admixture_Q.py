import os
import sys
import logging
import typer
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='a')
logging.info("The command line is:\n\tpython3{}".format(' '.join(sys.argv)))

def plot_admixture(dir: str = typer.Option(..., '--dir', '-d', help='包含所有Q文件的目录'),
                   sm : str = typer.Option(..., '--sm', '-s', help='样本名文件名,需要和fam文件一一对应'),
                   out: str = typer.Option(..., '--out', '-o', help='输出文件名')):
    """
    绘制admixture的结果
    """
    # 指定含有 .Q 文件的目录
    directory = dir

    # 读取样本名文件，每行一个样本名
    sample_names_file = sm
    with open(sample_names_file, 'r') as f:
        sample_names = f.read().strip().split('\n')

    # 获取所有 .Q 文件
    q_files = [f for f in os.listdir(directory) if f.endswith('.Q')]
    q_files.sort()  # 确保文件是按顺序排列的

    # 预定义一组颜色
    colors = ['#1f77b4', '#d62728', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # 确定图表的行数和列数
    n_rows = len(q_files)
    fig, axs = plt.subplots(n_rows, 1, figsize=(10, n_rows*2), sharex=True)  # 每个子图的高度为2，共享x轴

    # 遍历每个 .Q 文件，并绘制条形图
    for i, q_file in enumerate(q_files):
        df = pd.read_csv(os.path.join(directory, q_file), sep=' ', header=None)

        for j in range(df.shape[1]):
            bottom = df.iloc[:, :j].sum(axis=1) if j > 0 else None
            axs[i].bar(range(df.shape[0]), df.iloc[:, j], bottom=bottom, color=colors[j % len(colors)], width=1.0)
        
        # 为每个子图设置固定的y轴刻度
        axs[i].set_yticks([0, 0.25, 0.5, 0.75, 1])
        axs[i].set_yticklabels(['0', '0.25', '0.5', '0.75', '1'])
        
        # 设置 y 轴的标签
        axs[i].set_ylabel('Proportion', fontsize=10)
        
        # 设置每个子图的标题为K值
        k_value = q_file.split('.')[-2]
        axs[i].set_title(f'K = {k_value}')

        # 设置边距
        axs[i].margins(x=0.00)  # 减少左右两边的空白区域
        
    # 为整个图形设置标题
    fig.suptitle('Admixture Proportions by Individual for Different K Values')

        
    # 设置最底部子图的X轴标签为样本名
    axs[-1].set_xticks(range(len(sample_names)))
    axs[-1].set_xticklabels(sample_names, rotation=90, fontsize=8)  # 根据需要调整字体大小

    # 调整子图间距和边距
    plt.subplots_adjust(hspace=0.5, left=0.1, right=0.95, bottom=0.2)

    # 保存大图
    plt.savefig(out, dpi=300)

if __name__ == '__main__':
    typer.run(plot_admixture)
