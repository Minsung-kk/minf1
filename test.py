import os, os.path
import string
import random
import csv
import pandas as pd
import zipfile
import numpy as np
from PIL import Image
from sklearn.model_selection import KFold

from sklearn.metrics import confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt


clips = {'minsung': ['20210923_155848', '20210923_161107'], 'priya': ['20210923_163035', '20210923_163801'], 'fadl': ['20211001_152746', '20211001_154310']}

split = []
data_all = {}
m = {}
p = {}
f = {}
min = []
pri = []
fa = []
sp = {0:[], 1:[], 2:[], 3:[], 4:[]}

file = '/Users/minsungkim/Downloads/datasets/ug_data/ug_list.csv'
data_dir = '/Users/minsungkim/Downloads/datasets/ug_data/'
label_dir = '/Users/minsungkim/Downloads/datasets/'

# df = pd.read_csv(file)

# # separate by each person
# # clip, header, total frame, action number
# for index, row in df.iterrows():
#     data = [row[0], row[2], row[3]]
#     data_all[row[1]] = data
#     if row[0] in clips['minsung']:
#         min.append(data)
#     elif row[0] in clips['priya']:
#         pri.append(data)
#     elif row[0] in clips['fadl']:
#         fa.append(data)
# # print(data_all)

# for index, row in df.iterrows():
#     # print(row[0])
#     if row[0] in clips['minsung']:
#         try:
#             m[row[3]].append(row[1])
#         except:
#             m[row[3]] = [row[1]]
#     elif row[0] in clips['priya']:
#         try:
#             p[row[3]].append(row[1])
#         except:
#             p[row[3]] = [row[1]]
#     elif row[0] in clips['fadl']:
#         try:
#             f[row[3]].append(row[1])
#         except:
#             f[row[3]] = [row[1]]

# dict = [m, p, f]
# for j in dict:
#     for action, headers in j.items():
#         # print(headers)
#         random.shuffle(headers)
#         # print(headers)
#         length = len(headers)
#         splits = np.array_split(headers, 5)
#         for i in range(5):
#             sp[i].extend(splits[i])
#             print(i)
#             print(action, len(splits[i]))



# 5 fold train and valid
# data_colab_dir = '/content/datasets/ug_data/'
# for i in range(5):
#     train = [*range(0,5)]
#     val = i
#     train.remove(i)
#     with open(label_dir+'train_'+'sp'+str(i)+'.txt', 'w', newline='') as f:
#         for j in train:
#             for k in sp[j]:
#                 clip, total_frame, action_num = data_all[k]
#                 # print(clip, total_frame, action)
#                 data = data_colab_dir + k + ' ' + str(total_frame) + ' ' + str(action_num) + '\n'
#                 # print(data)
#                 f.write(data)
#     with open(label_dir+'val_'+'sp'+str(i)+'.txt', 'w', newline='') as f:
#         for l in sp[i]:
#             clip, total_frame, action_num = data_all[l]
#             # print(clip, total_frame, action)
#             data = data_colab_dir + l + ' ' + str(total_frame) + ' ' + str(action_num) + '\n'
#             # print(data)
#             f.write(data)

# for 
# cv = KFold(n_splits=5, random_state=1, shuffle=True)

# print(cv)
# print(cv.get_n_splits(m[0]))
# print(m[0])
# for train, test in cv.split(m[0]):
#     print('tra: ', len(train))
#     print('test: ', len(test))


def get_random_string(length):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    # With combination of lower and upper case
    result_str = ''.join(random.choice(characters) for i in range(length))
    # print random string
    print(result_str)

# get_random_string(8)

# path = '/Volumes/ETC/MInf/20210531_150448.zip'
# path_test = '/Users/minsungkim/Downloads/20210531_150448.zip'
# archive = zipfile.ZipFile(path)
# file_name =  str(1000).zfill(10)
# file_name = 'rgb/' + file_name + '.png'
# file = archive.open(file_name)
# image = Image.open(file)
# image.show()

# corrupted = []
# a = 'abdc'
# b = 'ggg'
# c = 'dawda'
# corrupted.append(a + b + c)

def file_count(dir):
    initial_count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    return initial_count-1

# df = df.drop(df[df.clip == '20210531_150448'].index)
# df = df.drop(df[df.clip == '20210603_130948'].index)

# corrupted_heads = ['2_yHpGSVwC','2_3TxTYKFT', '2_62YNmjEX', '2_yH42Ciyo','2_YBQCMVXu',
# '2_19JPf635', '2_qP97qWeZ', '2_kI6qnrfa', '2_Rsh9obtD', '2_tkOIAg4S', '2_1sFh4DtK', '2_P9Gxiw78',
# '2_vddKyVfB', '2_XXp7RhkO', '2_nW6Rvhxg', '2_1cWn8FpR', '2_iyaOxpFW', '2_hZOPcSL0', 
# ]
def create_list(csv_file):
    with open(data_dir+'ug_list.csv', 'w', newline='') as f:
        df = pd.read_csv(csv_file, usecols=['clip','header','action'])
        writer = csv.writer(f)
        writer.writerow(['clip', 'header', 'total_frame', 'action'])
        for index, row in df.iterrows():
            try:
                dir = '/Users/minsungkim/Downloads/datasets/ug_data/'
                clip = row['clip']
                header = row['header']
                action = row['action']
                total_frame = file_count(dir+header+'/')
                data = [clip, header, total_frame, action]
                writer.writerow(data) 
            except:
                continue
sp1_path = '/Users/minsungkim/Downloads/datasets/pg_sp4.csv'
ug_path = '/Users/minsungkim/Downloads/datasets/ug_list.csv'
# create_list(ug_path)
# dir = '/Users/minsungkim/Downloads/datasets/ug_data/1_0fCO8DNO/'


y_pred = [1,2,3,4]
y_true = [1,2,2,2]
classes = [*range(4)]
print(classes)

cf_matrix = confusion_matrix(y_true, y_pred)
df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix) *10, index = [i for i in classes],
                     columns = [i for i in classes])
plt.figure(figsize = (12,7))
sn.heatmap(df_cm, annot=True)
plt.savefig('/Users/minsungkim/Downloads/datasets/output.png')