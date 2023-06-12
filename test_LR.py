import os , pandas as pd, joblib, numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler,RobustScaler
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
model_save_path = os.path.join(current_path,"files/model.pkl")
"""设置绘图环境"""
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
sb.set(palette="muted", color_codes=True, font='SimHei', font_scale=0.8)

# --------1. 获取训练数据
print("正在读取训练数据......")
data = pd.read_excel(save_path)
#trianing_data_x = data.drop(data.columns[range(-3, 10)],axis = 1)
trianing_data_x = data.loc[:, "缸孔销温度3喷涂前的计测值"]
min = trianing_data_x.min()
max = trianing_data_x.max()
trianing_data_y = data.loc[:,"DC实修"]
X_train,X_test,Y_train,Y_test = train_test_split(trianing_data_x,trianing_data_y,train_size=0.8)
# transfer = StandardScaler()
# trianing_data_tx = transfer.fit_transform(trianing_data_x)


# -----------二、将 训练数据 和 测试数据 用散点图表示出来
plt.scatter(X_train,Y_train,color='b',label='train data')
#plt.scatter(X_test,Y_test,color='r',label='teat data')

#plt.legend(loc=2)
plt.xlabel('压铸参数计测值')
plt.ylabel('品质质量')

plt.show()

# ------------------ 三、建立训练模型
# 引入逻辑回归算法，并创建逻辑回归模型
model = LogisticRegression()
model = LogisticRegression(max_iter=3000, solver='liblinear', penalty='l2', C =0.5)
'''
sklearn 要求输入的特征为：二维数组类型，目前只有一个特征，要用 reshape 转换成 二维数组类型；
reshape(-1,1) 就是改变成 1列的数组，这个数组的长度是根据原始数组的大小自动形成的。
'''
X_train = X_train.values.reshape(-1,1)
X_test = X_test.values.reshape(-1,1)
model.fit(X_train,Y_train)
# print(model.fit(X_train,Y_train))
# 
# model.fit(trianing_data_tx,trianing_data_y)

# print(model.coef_[0].flatten())
# coef = pd.DataFrame({'var' : pd.Series(trianing_data_x.columns),
#                 'coef' : (pd.Series(model.coef_[0].flatten()))
#                 })
# coef = coef.iloc[coef['coef'].abs().argsort()[::-1]]
# print("训练参数影响因子：")
# print(coef)
print("Class:",model.classes_)
print("Coef:",model.coef_)
print("intercept",model.intercept_)
print("n_iter",model.n_iter_)

# 2.3 也可以用 model.predict() 函数得到的预测结果；
pred = model.predict(X_test)
print(X_test)
print('*'*20)
pred = pd.DataFrame(pred)
print(pred)

# 2.4 为了更深刻理解逻辑函数，根据逻辑回归函数及回归方程计算逻辑函数y值
# 截距
a = model.intercept_[0]
# 回归系数
b = model.coef_[0][0]
x = np.arange(0,100,0.01)
z = a+b*x
y_pred = 1/(1+np.exp(-z))

sb.lineplot(x=x, y=y_pred, label = '预测曲线')
plt.show()   