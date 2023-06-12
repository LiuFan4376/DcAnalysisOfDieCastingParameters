import pandas as pd
import numpy as np
import os, xlrd, requests, json
import seaborn as sb
import matplotlib.pyplot as plt
from util.http_request import *
from util.data_process import *
from util.data_visualization import Data_Visualization_util
# -----参数设置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
sb.set(palette="muted", color_codes=True, font='SimHei', font_scale=0.8)

current_path = os.path.abspath(os.path.dirname(__file__))
save_path1 = os.path.join(current_path, "files/铸造产品分析.xls")
save_path2 = os.path.join(current_path, "files/铸造生产过程.xls")
save_path = os.path.join(current_path, "files/data.xlsx")


data = pd.read_excel(save_path)


# data0 = data.query("质量等级 == 0 ")
# data1 = data.query("质量等级 == 1")
# data2 = data.query("质量等级 == 2")
sb.boxplot(x="质量等级", y="JET COOl 冷却水流量计测值4", data=data, palette="Set3")
plt.show()
