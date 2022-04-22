from tkinter import font
import matplotlib.pyplot as plt
import numpy as np

x = np.array(['0.01', '0.001', '0.0001'])
y_sgd =np.array([0.8390, 0.8405, 0.8073])
y_adam = np.array([0.2326, 0.8339, 0.8306])



font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)

data_dict = {'x':x, 'y_sgd':y_sgd, 'y_adam':y_adam}
fontdict = {'size':14}
plt.plot(x, y_sgd , 'b--o',label='SGD')
plt.plot(x, y_adam, 'r--o', label='Adam')
plt.xlabel('Learning Rate', fontdict=fontdict)
plt.ylabel('Accuracy', labelpad=5, fontdict=fontdict)
plt.legend()
plt.show()

x = np.array(['0.01', '0.001', '0.0001'])
y_sgd =np.array([0.2028, 0.3396, 0.2618])
y_adam = np.array([0.0884, 0.2005, 0.0])



font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)

data_dict = {'x':x, 'y_sgd':y_sgd, 'y_adam':y_adam}
fontdict = {'size':14}
plt.plot(x, y_sgd , 'b--o',label='SGD')
plt.plot(x, y_adam, 'r--o', label='Adam')
plt.xlabel('Learning Rate', fontdict=fontdict)
plt.ylabel('Accuracy', labelpad=5, fontdict=fontdict)
plt.legend()
plt.show()

x = np.array(['0.01', '0.001', '0.0001'])
y_sgd =np.array([0.5652, 0.5913, 0.5275])
y_adam = np.array([0.3333, 0.4899, 0.5913])



font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)

data_dict = {'x':x, 'y_sgd':y_sgd, 'y_adam':y_adam}
fontdict = {'size':14}
plt.plot(x, y_sgd , 'b--o',label='SGD')
plt.plot(x, y_adam, 'r--o', label='Adam')
plt.xlabel('Learning Rate', fontdict=fontdict)
plt.ylabel('Accuracy', labelpad=5, fontdict=fontdict)
plt.legend()
plt.show()