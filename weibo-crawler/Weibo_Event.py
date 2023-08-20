import shutil
import csv
import os
import pandas as pd
from datetime import date

import pandas as pd

import pandas as pd
from datetime import datetime


def merge_csv_files(directory):
    merged_data = []
    header = None
    original_header = None

    # 先获取所有子目录
    subdirs = next(os.walk(directory))[1]
    print(subdirs)

    for subdir in subdirs:
        print(subdir)
        subdir_path = os.path.join(directory, subdir)

        for file in os.listdir(subdir_path):
            if file.endswith(".csv") and file != "users.csv":

                filepath = os.path.join(subdir_path, file)

                # 在读取文件前关闭文件
                with open(filepath, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    current_header = next(reader)

                    if header is None:
                        header = current_header.copy()
                        header.append('Time')
                        header.append('WeiboID')
                        merged_data.append(header)
                        original_header = current_header

                    if current_header == original_header:
                        for row in reader:
                            row.append(subdir)
                            merged_data.append(row)

                    print(len(merged_data),merged_data[-1])

    output_directory = "weibo_event"
    os.makedirs(output_directory, exist_ok=True)

    today = date.today()
    filename = f"{today}.csv"
    output_filepath = os.path.join(output_directory, filename)

    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(merged_data)

    shutil.rmtree(directory)


def proceed_csv():

    today = date.today()
    filename = f"{today}.csv"
    file_path = os.path.join("weibo_event", filename)

    # 打开 CSV 文件
    df = pd.read_csv(file_path, encoding='utf-8-sig', index_col=False)

    # 打印 DataFrame
    print(df)

    # 打印 '正文' 列的值
    print(df['正文'])

    # 删除指定列
    df = df.drop(columns=['id', 'bid', '头条文章url', '原始图片url', '视频url', '位置','@用户', '工具'])

    # 将 WeiboID 列放在第一列
    columns = df.columns.tolist()
    columns.remove('WeiboID')
    columns.insert(0, 'WeiboID')
    df = df[columns]

    # 保存修改后的 DataFrame 到 CSV 文件
    df.to_csv(file_path, index=False)



if __name__ == "__main__":
    weibo_directory = "weibo"
    os.system("python weibo.py")
    merge_csv_files(weibo_directory)
    proceed_csv()

