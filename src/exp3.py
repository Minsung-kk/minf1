import os
import utils
import pandas as pd
import csv
import numpy as np

colab_dir = '/content/datasets/'
csv_path = '/Users/minsungkim/Downloads/datasets/'
clips = {'minsung': ['20210923_155848', '20210923_161107'], 'priya': ['20210923_163035', '20210923_163801'], 'fadl': ['20211001_152746', '20211001_154310']}

# ug data
def create_label_ug(csv_path, seq):
    df = pd.read_csv(csv_path+'ug_list.csv')
    min = {}
    fadl = {}
    priya = {}
    test_label = []
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
        if row[0] in clips['minsung'][seq]:
            try:
                min[row[3]].append(label) 
            except:
                min[row[3]] = [label]
        elif row[0] in clips['minsung'][(seq+1)%2]:
            test_label.append(label)
        # fadl
        elif row[0] in clips['fadl'][seq]:
            try:
                fadl[row[3]].append(label) 
            except:
                fadl[row[3]] = [label]
        elif row[0] in clips['fadl'][(seq+1)%2]:
            test_label.append(label)
        # priya
        elif row[0] in clips['priya'][seq]:
            try:
                priya[row[3]].append(label) 
            except:
                priya[row[3]] = [label]       
        elif row[0] in clips['priya'][(seq+1)%2]:
            test_label.append(label)           
    # count = {}
    # name = fadl
    # for i in range(10):
    #     try:
    #         count[i] = len(name[i])
    #     except:
    #         continue
    # print(count)
    # count = {}
    # name = fadl_test
    # for i in range(10):
    #     try:
    #         count[i] = len(name[i])
    #     except:
    #         continue
    # print(count)
    
    # train label, test label
    data_all = {0:[], 1:[], 2:[], 3:[]}
    for name in [min, fadl, priya]:
        for i in name:
            pre_data = name[i]
            data = np.array_split(pre_data,4)
            for j in range(4):
                data_all[j].extend(data[j])
    train_label = []
    for i in data_all:
        train_label.append(data_all[i])
    
    # print(len(ret_data))
    return train_label, test_label

train, test = create_label_ug(csv_path, 0)
print(len(train))
print(len(test))
# train, test = create_label_ug(csv_path, 1)
# print(len(train))
# print(len(test))

# write a txt file with data
def create_annot(train_label, test_label):
    for i in range(4):
        train = []        
        fold = [*range(4)]
        val = train_label[i]
        fold.pop(i)

        for j in fold:
            train.extend(train_label[j])        
        with open(csv_path+'exp3/train_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in train:
                annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
        with open(csv_path+'exp3/val_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in val:
                annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)

    test = test_label
    with open(csv_path+'exp3/test.txt', 'w', newline='') as f:
        for j in test:
            annot = colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
            f.write(annot)
    
create_annot(train, test)
