""" store에 저장된 csv 파일에 저장된 마지막 연도별로 분류해주는 스크립트"""
import csv
import os
import shutil

storage_file = "./store"

csv_files = [name for name in os.listdir(storage_file)]

last_info = []

for csv_file in csv_files:
    with open(storage_file + "/" + csv_file, "r", encoding="utf8") as f:
        result = csv.reader(f, delimiter=",")

        last_index = [row for row in result]

        a = last_index[-1]

        a.append(csv_file)

        last_info.append(a)

for row in last_info:

    year = row[0].split('-')[0]

    save_folder = storage_file + "/" + year

    try:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
    except:
        pass

    src = storage_file + "/" + row[-1]
    dst = save_folder

    shutil.move(src, dst)
