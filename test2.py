import os , pandas as pd, numpy as np
from util.query_set import QuerySet
from util.console_interation import *
from util.data_process import *
from util.http_request import *
from math import ceil
from util.data_visualization import *
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
# 生成示例数据
current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
save_path1=os.path.join(current_path,"files/铸造产品分析.xlsx")
save_path2=os.path.join(current_path,"files/铸造压铸过程.xlsx")
statistic_data_path = os.path.join(current_path,"files/统计量分析结果.xls")

plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
sb.set(palette="muted", color_codes=True, font='SimHei', font_scale=0.8)

parameter = "V3计测值"
statistic_data = pd.read_excel(statistic_data_path)
col = statistic_data.columns
axis_x = col[25:28]
#print(statistic_data.loc["V3计测值",col[1,2,3]])
print(statistic_data.index)
ax =sb.barplot(x=axis_x, y = statistic_data.iloc[8,25:28])
for i in ax.containers:
    ax.bar_label(i,)
plt.ylabel(statistic_data.iloc[8,0])
plt.show()

