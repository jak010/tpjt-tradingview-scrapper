import os
import csv

storage_file = "/Users/jako/tesnine/opt/trading_view_scrapper/store"

csv_files = [name for name in os.listdir(storage_file)]

last_info = []

for csv_file in csv_files:
    with open(storage_file + "/" + csv_file, "r", encoding="utf8") as f:
        result = csv.reader(f, delimiter=",")

        # humanize_times = [row[0] for row in result]
        last_index = [row for row in result]

        a = last_index[-1]

        a.append(csv_file)

        last_info.append(a)

from pprint import pprint

import shutil

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
