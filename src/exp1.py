import os
import utils
import pandas as pd
import csv
import numpy as np
colab_dir = '/content/datasets/'
csv_path = '/Users/minsungkim/Downloads/datasets/'
clips = {'minsung': ['20210923_155848', '20210923_161107'], 'priya': ['20210923_163035', '20210923_163801'], 'fadl': ['20211001_152746', '20211001_154310']}

def count_actions(labels):
    count = {}
    for i in labels:
        action = i[3]
        num = str(action)
        try:
            count[num] += 1
        except:
            count[num] = 1
    return dict(sorted(count.items(), key=lambda item: item[0]))

# def split(a, n):
#     k, m = divmod(len(a), n)
#     return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

# ug data
def create_label_ug(csv_path):
    df = pd.read_csv(csv_path+'ug_list.csv')
    min = {}
    fadl = {}
    priya = {}
    for index, row in df.iterrows():
        header = row[1]
        # exclude nonexistent data        
        if not os.path.isdir(csv_path+'ug_data/'+header):
            continue       
        total_frame = str(row[2])
        # exclude data having less than 5 images
        if int(total_frame) < 5:
            continue
        action_num = str(row[3])
        label = [header, total_frame, action_num]
        # minsung
        if row[0] in clips['minsung']:
            try:
                min[row[3]].append(label) 
            except:
                min[row[3]] = [label]
        # fadl
        if row[0] in clips['fadl']:
            try:
                fadl[row[3]].append(label) 
            except:
                fadl[row[3]] = [label]
        # minsung
        if row[0] in clips['priya']:
            try:
                priya[row[3]].append(label) 
            except:
                priya[row[3]] = [label]                   
    count = {}
    name = min
    for i in range(10):
        try:
            count[i] = len(name[i])
        except:
            continue
    # print(count)
    data_all = {0:[], 1:[], 2:[], 3:[], 4:[]}
    for name in [min, fadl, priya]:
        for i in name:
            pre_data = name[i]
            data = np.array_split(pre_data,5)
            for j in range(5):
                data_all[j].extend(data[j])
    ret_data = []
    for i in data_all:
        ret_data.append(data_all[i])
    # print(len(ret_data))
    return ret_data

# read ug and pg csv and return lists for each person sorted by action
def create_label(csv_path):
    data_all = []
    for i in range(5):
        data = []
        # pg data
        df = pd.read_csv(csv_path+'pg_sp' + str(i) + '.csv')
        for index, row in df.iterrows():
            header = row[1]
            # exclude nonexistent data
            if not os.path.isdir(csv_path+'pg_data/'+header):
                continue       
            total_frame = str(row[2])
            # exclude data having less than 5 images
            if int(total_frame) < 5:
                continue
            action_num = str(row[3])
            data.append([header, total_frame, action_num])
        # print(data)
        data_all.append(data)
    # print(len(data_all))
    ug_data = create_label_ug(csv_path)
    for i in range(5):
        data_all.extend(ug_data[i])
        
    return data_all

# write a txt file with data
def create_annot(label):
    for i in range(5):
        train = []        
        fold = [*range(5)]
        val = label[i]
        test = label[(i+1)%5]

        # print(fold)
        fold.pop(i)
        fold.pop(i%4)
        # print(fold)
        for j in fold:
            train.extend(label[j])        
        with open(csv_path+'exp1/train_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in train:
                annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
        with open(csv_path+'exp1/val_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in val:
                annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
        with open(csv_path+'exp1/test_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in test:
                annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
    
label = create_label(csv_path)
ug_label = create_label_ug(csv_path)
for i in range(5):
    label[i] = label[i] + ug_label[i]

create_annot(label)


# def create():
#     data = []
#     for i in range(5):
#         df = pd.read_csv(annot_dir+'ug_list.csv')
#         for index, row in df.iterrows():
#             clip = row[0]
#             header = row[1]
#             total_frame = str(row[2])
#             action_num = str(row[3])
#             data.append([clip, header, total_frame, action_num])
#     # make dictionaries for each person
#     min = {}
#     priya = {}
#     fadl = {}
#     for j in data:
#         if row[0] in utils.clips['minsung']:
#             try:
#                 min[row[3]].append(row[1])
#             except:
#                 min[row[3]] = [row[1]]
#         elif row[0] in utils.clips['priya']:
#             pri.append(data)
#         elif row[0] in utils.clips['fadl']:
#             fa.append(data)
#     return data