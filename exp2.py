import os
import utils
import pandas as pd
import csv

# locations
annot_dir = '/Users/minsungkim/Downloads/datasets/'
ug_colab_dir = '/content/datasets/ug_data/'
pg_colab_dir = '/content/datasets/pg_data/'


""" 
exp2: use ug 5-fold to train, use all pg to test
"""
# make a exp2 directory
utils.create_directory(annot_dir+'exp2/')

# create 5 fold annotation from pg data
def create_train_annot(annot_path):
    data_all = []
    for i in range(5):
        data = []
        df = pd.read_csv(annot_path+'pg_sp' + str(i) + '.csv')
        for index, row in df.iterrows():
            header = row[1]
            # exclude nonexistent data
            if not os.path.isdir(annot_dir+'pg_data/'+header):
                continue       
            total_frame = str(row[2])
            # exclude data having less than 5 images
            if int(total_frame) < 5:
                continue
            action_num = str(row[3])
            data.append([header, total_frame, action_num])
        # print(data)
        data_all.append(data)
        # write a txt file with data
    for i in range(5):
        train = []
        val = []
        fold = [*range(5)]
        val = data_all[i]
        fold.pop(i)
        # print(fold)
        # print(val[:2])
        # print(len(val))
        for j in fold:
            train.extend(data_all[j])
        # print(train[:2])
        # print(len(train))             
        with open(annot_path+'exp2/train_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in train:
                annot = pg_colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
        with open(annot_path+'exp2/val_sp' + str(i) + '.txt', 'w', newline='') as f:
            for j in val:
                annot = pg_colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
                f.write(annot)
    return data_all

# test annotation file which consists of all pg data
def create_test_annot(annot_path):
    data = []
    count = 0
    # read all split csvs and save at data
    # for i in range(5):
    df = pd.read_csv(annot_path+'ug_list.csv')
    for index, row in df.iterrows():
        header = row[1]
        # exclude nonexistent data
        if not os.path.isdir(annot_dir+'ug_data/'+header):
            continue       
        total_frame = str(row[2])
        # exclude data having less than 2 images
        if int(total_frame) < 1:
            continue
        action_num = str(row[3])
        data.append([header, total_frame, action_num])
    # write a txt file with data
    with open(annot_path+'exp2/test.txt', 'w', newline='') as f:
        for j in data:
            annot = ug_colab_dir + j[0] + ' ' + j[1] + ' ' + j[2] + '\n'
            f.write(annot)

create_train_annot(annot_dir)
# print(create_train_annot(annot_dir))
create_test_annot(annot_dir)


'''
test - by loading pth files
sp0: 
epoch=10, lr= 0.001, batch size=4
top1_acc: 0.2783
top5_acc: 0.7571
mean_class_accuracy: 0.1138

epoch=15, lr= 0.001, batch size=4
top1_acc: 0.3208
top5_acc: 0.7465
mean_class_accuracy: 0.1180

epoch=20, lr= 0.001, batch size=4
top1_acc: 0.3031
top5_acc: 0.7488
mean_class_accuracy: 0.1101

epoch=100, lr= 0.001, batch size=4
top1_acc: 0.3455
top5_acc: 0.7465
mean_class_accuracy: 0.1235


sp1:
eopch=15, lr= 0.001, batch size=4
top1_acc: 0.2429
top5_acc: 0.7028
mean_class_accuracy: 0.0910

eopch=20, lr= 0.001, batch size=4
top1_acc: 0.3502
top5_acc: 0.7712
mean_class_accuracy: 0.1430

epoch=25, lr= 0.001, batch size=4
top1_acc: 0.3290
top5_acc: 0.7559
mean_class_accuracy: 0.1285

sp2:
eopch=10, lr= 0.001, batch size=4
top1_acc: 0.1840
top5_acc: 0.7476
mean_class_accuracy: 0.0749

eopch=20, lr= 0.001, batch size=4
top1_acc: 0.2948
top5_acc: 0.7193
mean_class_accuracy: 0.1091

eopch=25, lr= 0.001, batch size=4
top1_acc: 0.3502
top5_acc: 0.7712
mean_class_accuracy: 0.1430

sp3:
eopch=20, lr= 0.001, batch size=4
top1_acc: 0.3149
top5_acc: 0.7465
mean_class_accuracy: 0.1243

eopch=25, lr= 0.001, batch size=4
top1_acc: 0.2771
top5_acc: 0.6910
mean_class_accuracy: 0.1030

eopch=30, lr= 0.001, batch size=4
top1_acc: 0.2948
top5_acc: 0.7925
mean_class_accuracy: 0.1042

sp4:
eopch=20, lr= 0.001, batch size=4
top1_acc: 0.2866
top5_acc: 0.7842
mean_class_accuracy: 0.1192

eopch=25, lr= 0.001, batch size=4
top1_acc: 0.3054
top5_acc: 0.7524
mean_class_accuracy: 0.1218
'''