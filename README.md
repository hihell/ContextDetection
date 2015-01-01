PostureDetection
================

data文件夹下是数据


main.py中
---------
train方法，参数是分类器和训练数据路径
predict方法，参数是训练好的分类器和需要预测的数据路径

train方法执行的时候会进行cross validation

utilsPlot.py中
--------------
plotExample方法，显示加速传感器的图像，参数是数据路径
