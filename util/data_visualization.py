import pandas as pd
import numpy as np
import os, xlrd, requests, json
import seaborn as sb
import matplotlib.pyplot as plt

def set_plot_environment():
    """设置绘图环境"""
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
    sb.set(palette="muted", color_codes=True, font='SimHei', font_scale=0.8)
    
class Data_Visualization_util:
    def __init__(self, data, data0, data1, data2):
        self.data = data
        self.data0 = data0
        self.data1 = data1
        self.data2 = data2
        
    def plot_distribution_curve(self, parameter):
        """绘制分布曲线

        Args:
            parameter (string): 要进行分析的压铸参数

        Returns:
        """
        set_plot_environment()
        statistic_parameter = parameter
        statistic_data = self.data.loc[:, statistic_parameter]
        statistic_data0 = self.data0.loc[:, statistic_parameter]
        statistic_data1 = self.data1.loc[:, statistic_parameter]
        statistic_data2 = self.data2.loc[:, statistic_parameter]

        min_value = self.data.loc[:, statistic_parameter].min()
        max_value = self.data.loc[:, statistic_parameter].max()
        step = (max_value - min_value)/50
        x_lable = np.arange(min_value, max_value, step)
        x_axis = [0 for i in range(0, len(x_lable-1))]
        count_data = np.zeros(len(x_lable))
        count_data0 = np.zeros(len(x_lable))
        count_data1 = np.zeros(len(x_lable))
        count_data2 = np.zeros(len(x_lable))
        for index in range(0,len(x_lable)-1):
            start_value = x_lable[index]
            if(index == len(x_lable)-1):
                end_value = start_value + step
            else:
                end_value = x_lable[index+1]
            x_axis[index] = str(round(np.float64(start_value), 3))+"~"+str(round(np.float64(end_value), 3))
            count_data[index] = np.sum((statistic_data>=start_value)&(statistic_data<end_value))
            count_data0[index] = np.sum((statistic_data0>=start_value)&(statistic_data0<end_value))
            count_data1[index] = np.sum((statistic_data1>=start_value)&(statistic_data1<end_value))
            count_data2[index] = np.sum((statistic_data2>=start_value)&(statistic_data2<end_value))
        MC_return0_ratio = np.zeros(len(x_lable))
        DC_do0_ratio = np.zeros(len(x_lable))
        DC_do1_ratio = np.zeros(len(x_lable))

        for i in range(0,len(count_data)-1):
            if(not count_data[i]==0):
                MC_return0_ratio[i] = count_data0[i]/count_data[i]
                DC_do0_ratio[i] = count_data1[i]/count_data[i]
                DC_do1_ratio[i] = count_data2[i]/count_data[i]

        ratio_table = pd.DataFrame( columns=["压铸参数区间"], data=x_axis)
        ratio_table['数据条数'] = count_data 
        ratio_table['MC返回为0比率'] = MC_return0_ratio
        ratio_table['DC实修为0比率'] = DC_do0_ratio
        ratio_table['DC实修为1比率'] = DC_do1_ratio

        f = plt.figure()
        f.add_subplot(1,2,1)
        sb.barplot(x = ratio_table.loc[:, "压铸参数区间"], y=ratio_table.loc[:,"MC返回为0比率"], color = "skyblue", label = "MC返回为0比率")
        sb.barplot(x = ratio_table.loc[:, "压铸参数区间"], y=ratio_table.loc[:,"DC实修为0比率"], color = "yellow", label = "DC实修为0比率")
        sb.barplot(x=ratio_table.loc[:, "压铸参数区间"], y=ratio_table.loc[:, "DC实修为1比率"], color ="red", label = "DC实修为1比率")
        plt.legend()
        plt.ylabel("比率", fontsize = 10)
        plt.xlabel(parameter+"区间", fontsize = 10)
        plt.xticks(rotation = 270)
        f.add_subplot(1,2,2)
        sb.histplot(self.data0.loc[:, statistic_parameter], bins=100, kde=True, color="skyblue", label="MC为0")
        sb.histplot(self.data1.loc[:, statistic_parameter], bins=100, kde=True, color="yellow", label="MC返回为1,DC实修为0")
        sb.histplot(self.data2.loc[:, statistic_parameter], bins=100, kde=True, color="red", label="MC返回为1,DC实修为1")
        plt.legend()
        plt.ylabel("数据量")
        plt.show()
      