import numpy as np , os, pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

"""设置绘图环境"""
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
sb.set(palette="muted", color_codes=True, font='SimHei', font_scale=0.8)

current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
# -----数据过滤

print("正在读取训练数据......")
data = pd.read_excel(save_path)
#print(data.columns[10:len(data.columns)-3])
for parameter in data.columns[10:len(data.columns)-3]:
    data_column = data.loc[:,parameter]
    # 上四分位数
    up_q = data_column.quantile(0.75)
    # 下四分位数
    low_q = data_column.quantile(0.25)
    # k=1.5是个经验值，根据整体数据的离散程度调节。一般范围[1.5, 3)
    dis = 1.5*(up_q - low_q)
    # 上边界
    up_limit = up_q + dis
    # 下边界
    low_limit = low_q - dis
    data_column[(data_column>=up_limit)|(data_column<=low_limit)] = np.nan
    data.loc[:,parameter] =data_column
    print(data.loc[:,parameter])
data.dropna(how='all', axis=1,inplace=True)
data.to_excel(current_path+"/test.xlsx")
    