import typer
import os
import sys
import logging

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='a')
logging.info("The command line is:\n\tpython3{}".format(' '.join(sys.argv)))


def compare_lists(list1, list2):
    # 比较两个列表中相同元素的数量
    if len(list1) != len(list2):
        return False
    # 统计相同基因型的数量
    same = sum(1 for item1, item2 in zip(list1, list2) if item1 == item2 and item1 != '00')
    total = len(list1)  # 总共的比较次数
    return [same, total]

def compare_genotypes(ped: typer.FileText = typer.Option(..., '--ped', '-p', help='PED file containing all samples to be compared'),
                      lst: typer.FileText = typer.Option(..., '--lst', '-l', help='List of sample pairs to be compared'),
                      out: typer.FileTextWrite  = typer.Option(..., '--out', '-o', help='Output file name')):
    '''
    比较指定样本之间的基因型一致率。
    --ped: 标准PLINK格式的PED文件。
    --lst: 指定样本名，例如：ALT1  ALT2, ALT2  ALT3。
    '''
    # 从PED文件中读取样本基因型信息
    iid_gt_dct = {line.split()[1]: [line.split()[6:][i:i+2] for i in range(0, len(line.split()), 2)] for line in ped}

    # 遍历LIST文件中的样本对，进行比较
    for line in lst:
        id1, id2 = line.strip().split()[:2]
        # 获取两个样本的基因型信息
        gt1, gt2 = iid_gt_dct.get(id1, [['00']*2]), iid_gt_dct.get(id2, [['00']*2])
        num_lst = compare_lists(gt1, gt2)
        # 写入结果到输出文件
        out.write('\t'.join([id1, id2, str(num_lst[0]), str(num_lst[1]), f"{num_lst[0]/num_lst[1]:.4f}"]) + '\n')

if __name__ == '__main__':
    typer.run(compare_genotypes)

