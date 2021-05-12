import pandas as pd
import numpy as np
import re
from collections import Counter
import os

import matplotlib.pyplot as plt
from matplotlib import cm

os.system("cls")
csv_path = input("csv 파일 경로를 입력해주세요(해당 파일 포함): ")
column_name = input("시군별 빈도수를 확인할 컬럼의 이름을 입력해주세요: ")
graph_title = input("출력할 그래프의 제목을 입력해주세요: ")
graph_color = input("출력할 그래프의 색 그라이언트 종류 이름을 입력해주세요('https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html' 사이트 참고, \n기본값: 0, 특이함: 1): ")
graph_file_name = input("출력할 그래프의 파일 이름을 입력해주세요(확장자 제외): ")

plt.style.use("seaborn")
plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

if graph_color == "1":
    graph_color = "cubehelix_r"

df1 = pd.read_csv(csv_path, encoding="cp949")
df1.fillna("", inplace=True)
city_names = list(map(lambda x: "".join(re.sub("^\w+도 ", "", x)), df1[column_name].values))
city_names = list(map(lambda x: "".join(re.findall("^(\w+)", x)), city_names))
city_names_count = Counter(city_names)
city_names_count_df = pd.DataFrame({"시/군": list(city_names_count.keys()), "빈도수": list(city_names_count.values())})
city_names_count_df.loc[city_names_count_df["시/군"] == "", "시/군"] = "Missing"
city_names_count_df.sort_values("빈도수", ascending=False, inplace=True)
city_names_count_df.reset_index(drop=True, inplace=True)

fig, ax = plt.subplots(figsize=(10, 8), dpi=80)

if graph_color != "0":
    exec("colors = cm." + graph_color + "(np.linspace(0, 1, len(city_names_count_df.index)))")
    colors = colors[::-1]
    ax.barh(city_names_count_df.index, city_names_count_df["빈도수"], color=colors, align='center')
else:
    ax.barh(city_names_count_df.index, city_names_count_df["빈도수"], align='center')

ax.set_yticks(city_names_count_df.index)
ax.set_yticklabels(city_names_count_df["시/군"])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("빈도수")
ax.set_ylabel("시/군")
ax.set_title(graph_title)
plt.savefig(graph_file_name + ".png")

## activate virtual
## cd C:\Users\User\PycharmProjects\MyProject2
## pyinstaller --onefile "공공데이터 도시 빈도수 시각화 프로그램.py"
