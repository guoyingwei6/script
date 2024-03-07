import pandas as pd
import typer
import os
import sys
import logging
logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='a')
#logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")
logging.info("The command line is:\n\tpython3 {}".format(' '.join(sys.argv)))

app = typer.Typer()


@app.command()
def calculate_concordance(ped_file: str = typer.Option(..., '--ped', help="Path to the PED file"),
                          pairs_file: str = typer.Option(..., '--lst', help="Path to the file with pairs of sample IDs"),
                          output_file: str = typer.Option(..., '--out', help="Path to the output file")):
'''
不考虑是否缺失，否则时间太长了，一个缺失一个正常也算不一致的，两个都缺失算一致的，想要准确让缺失值都过去掉。输入文件直接用ped文件的compound格式。
'''
    # 读取PED文件，设置low_memory为False
    df = pd.read_csv(ped_file, sep="\s+", header=None, low_memory=False)
    # 提取样本ID和基因型数据
    ids = df[1]
    genotypes = df.iloc[:, 6:]

    # 读取需要比较的样本对
    pairs = pd.read_csv(pairs_file, sep="\t", header=None, names=["id1", "id2"])

    with open(output_file, "w") as f_out:
        f_out.write("id1\tid2\tmatching_snps\ttotal_snps\tconcordance\n")

        # 遍历每一对样本，计算一致性
        for _, row in pairs.iterrows():
            id1, id2 = row["id1"], row["id2"]
            if id1 not in ids.values or id2 not in ids.values:
                # 处理不存在的样本ID
                f_out.write(f"{id1}\t{id2}\tID not found\n")
                continue

            gt1 = genotypes[ids == id1].iloc[0]
            gt2 = genotypes[ids == id2].iloc[0]

            # 计算匹配和总SNP数
            matching_snps = (gt1 == gt2).sum()
            total_snps = len(gt1)

            # 计算一致率
            concordance = matching_snps / total_snps
            f_out.write(f"{id1}\t{id2}\t{matching_snps}\t{total_snps}\t{concordance:.4f}\n")

if __name__ == "__main__":
    app()

