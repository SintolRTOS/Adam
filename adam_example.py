# -*- coding: UTF-8 -*-
# author: wangjingyi
import sys
print(sys.version)
import autograd.numpy as np
from autograd import grad

EPOCHS = 1000

class Adam:
	#初始化
	def __init__(self, loss, weights, lr=0.001, beta1=0.9, beta2=0.999, epislon=1e-8):
		self.loss = loss
		self.theta = weights
		self.lr = lr
		self.beta1 = beta1
		self.beta2 = beta2
		self.epislon = epislon
		self.get_gradient = grad(loss)
		self.m = 0
		self.v = 0
		self.t = 0
	#最小化行
	def minimize_raw(self):
		self.t += 1
		g = self.get_gradient(self.theta)
		self.m = self.beta1 * self.m + (1 - self.beta1) * g
		self.v = self.beta2 * self.v + (1 - self.beta2) * (g * g)
		self.m_cat = self.m / (1 - self.beta1 ** self.t)
		self.v_cat = self.v / (1 - self.beta2 ** self.t)
		self.theta -= self.lr * self.m_cat / (self.v_cat ** 0.5 + self.epislon)
	
	#取最小值逼近
	def minimize(self):
		self.t += 1
		g = self.get_gradient(self.theta)
		lr = self.lr * (1 - self.beta2 ** self.t) ** 0.5 / (1 - self.beta1 ** self.t)
		self.m = self.beta1 * self.m + (1 - self.beta1) * g
		self.v = self.beta2 * self.v + (1 - self.beta2) * (g * g)
		self.theta -= lr * self.m / (self.v ** 0.5 + self.epislon)

	#显示最小损失
	def minimize_show(self, epochs=5000):
		for _ in range(epochs):
			self.t += 1
			g = self.get_gradient(self.theta)
			lr = self.lr * (1 - self.beta2 ** self.t) ** 0.5 / (1 - self.beta1 ** self.t)
			self.m = self.beta1 * self.m + (1 - self.beta1) * g
			self.v = self.beta2 * self.v + (1 - self.beta2) * (g * g)
			self.theta -= lr * self.m / (self.v ** 0.5 + self.epislon)
			print("step{: 4d} g:{} lr:{} m:{} v:{} theta:{}".format(self.t, g, lr, self.m, self.v, self.theta))

		final_loss = self.loss(self.theta)
		# print("final loss:{} weights:{}".format(final_loss, self.theta))

	#sigmoid函数计算
def sigmoid(x):
    return 0.5*(np.tanh(x) + 1)
	
	# 根据逻辑模型输出标签为真的概率
def logistic_predictions(weights, inputs):
    return sigmoid(np.dot(inputs, weights))

	# 培训损失是培训标签的负对数可能性.
def training_loss(weights):
    preds = logistic_predictions(weights, inputs)
    label_probabilities = preds * targets + (1 - preds) * (1 - targets)
    return -np.sum(np.log(label_probabilities))

# 构建一个测试数据集
inputs = np.array([[0.52, 1.12,  0.77],
                   [0.88, -1.08, 0.15],
                   [0.52, 0.06, -1.30],
                   [0.74, -2.49, 1.39]])
targets = np.array([True, True, False, True])
weights = np.array([0.0, 0.0, 0.0])

def sgd(epochs=1000):
	training_gradient_fun = grad(training_loss)
	# 使用梯度下降法优化权重.
	weights = np.array([0.0, 0.0, 0.0])
	print("Initial loss:{}".format(training_loss(weights)))
	for i in range(epochs):
	    weights -= training_gradient_fun(weights) * 0.01

	print("Trained loss:{}".format(training_loss(weights)))
	print("weights:{}".format(weights))

# 执行主函数
if __name__ == "__main__":
	adam = Adam(training_loss, weights, lr=0.01)
	print("start to optimize:")
	# adam.minimize_show(epochs=EPOCHS)

	for i in range(EPOCHS):
		adam.minimize_raw()
	print("weights:{} loss:{}".format(adam.theta, adam.loss(adam.theta)))