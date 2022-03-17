import csv
# from fileinput import filename
import copy
import os
from re import S
import zipfile
import pandas as pd
import string
import random
import shutil


from PIL import Image
import torchvision.transforms.functional as fn

def create_directory(dir_name):
    # Create target Directory if don't exist
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        # print("Directory " , dir_name ,  " Created ")
    else:    
        print("Directory " , dir_name ,  " already exists")

csv_location = '/Volumes/ETC/data_9classNother/'
file_names = ['sp1.csv', 'sp2.csv', 'sp3.csv', 'sp4.csv', 'sp5.csv']
for i in range(5):
    file_names[i] = csv_location + file_names[i]
# for i in file_names:
#     if i == 'sp1.csv':
#         pre_df = pd.read_csv(file_names[0], usecols=['Project'])
#         pre_df = pre_df.drop_duplicates()
#         print(len(pre_df))
#     else:
#         cur_df = pd.read_csv(i, usecols=['Project'])
#         cur_df = cur_df.drop_duplicates()
#         pre_df = pd.concat([pre_df, cur_df])
#         print(len(cur_df))

# pre_df = pre_df.drop_duplicates()
# pre_df = pre_df.sort_values(by=['Project'])
# print(pre_df)
# print(len(pre_df))

df = pd.read_csv(file_names[0], usecols=['Project','Action','Imgs'])
# sample = pd.read_csv(file_names[0], usecols=['Project'])
# sample2 = pd.read_csv(file_names[4], usecols=['Project'])
#         pre_df = pre_df.drop_duplicates()
#         print(len(pre_df))
# sample = df.loc[df['Project'] == '20210804_145925']
head = df.head()
head = head.reset_index()

# for index, row in df.iterrows():
#     if row['Project'] == '20210811_132135' and row['Action'] == 0:
#         print(row['Imgs'])


# maybe dictionary for folder names?
# action: count
# {'0':0, '1':0, ...}
labels = []

# for index, row in df.iterrows():
#     print(row['Action'])

def get_random_string(length):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    # With combination of lower and upper case
    result_str = ''.join(random.choice(characters) for i in range(length))
    # print random string
    return result_str

def create_label(file):
    # print(type(pre_img))
    label = []
    pre_img = file.iloc[0]['Imgs']
    pre_act = file.iloc[0]['Action']
    # print(pre_img)
    start_img = 0
    end_img = 0
    pre_project = file.iloc[0]['Project']
    track = []
    count = 0
    for index, row in file.iterrows():
    # for index, row in head.iterrows():  
        cur_act = row['Action']
        cur_img = row['Imgs']
        cur_project = row['Project']
        # print('pre: ', pre_img)
        # print('cur: ', cur_img)
        # print('prepro: ', pre_project)
        # print('curpro: ', cur_project)
        # print(count)
        
        # if cur_project == '20210530_153343' or cur_project == '20210609_221133':
        #     track.append([count, cur_project, cur_img])
        if (cur_img - pre_img) == 0 and (pre_project == cur_project) and (pre_act == cur_act):      
            start_img = cur_img

        elif (cur_img - pre_img) == 1 and (pre_project == cur_project) and (pre_act == cur_act): 
            pre_img = cur_img
        elif (pre_project != cur_project) and ((cur_img - pre_img) > 1 or (cur_img - pre_img) < 0): 
            # if cur_project == '20210530_153343' or cur_project == '20210609_221133':
            #     track.append([count, cur_project, cur_img, pre_project, pre_img])
            end_img = pre_img
            # track.append([pre_project, cur_project])
            label.append((pre_project, pre_act, start_img, end_img, '2_'+get_random_string(8)))
            start_img = cur_img
            pre_img = cur_img
            pre_project = cur_project
            pre_act = cur_act
            count+=1
    return label
    # if row['Project'] == '20210609_221133':
    #     print(cur_img)



# for i in labels:
#     print(i)
# print(len(labels))
# for i in track:
#     if i[0] == '20210609_221133' and i[1] > 3000:
#         print('here')
# print(track)
# print(labels[8])
# print(labels)

# print(labels[11])

# print(labels)
data_dir = '/Volumes/ETC/MInf/'
save_dir = '/Users/minsungkim/Downloads/datasets/'
image_dir = '/Users/minsungkim/Downloads/datasets/pg_data/'
# create an image directory
# create_directory(image_dir)


# test = [('20210531_150448', 5, 2271, 2283),]

# archive = zipfile.ZipFile(data_dir+test[0]+'.zip')
# c = 0
# for file in archive.namelist():
#         if file.startswith('rgb/') and file.endswith('.png'):
#             c+=1
# print(c)

# to check whether a zip file is ok. If not, write its name on a text file



def create_data(labels):
    # project_count = 0
    corrupted = []
    pre_act = 0
    for i in labels:
        project = i[0]
        action = i[1]
        start_frame = i[2]
        end_frame = i[3]
        header = i[4]

        if pre_act != action:
            # project_count = 0
            pre_act = action
        img_dir = image_dir + header + '/'
        create_directory(img_dir)
        # start_frame = str(i[2]).zfill(10)
        # end_frame = str(i[3]).zfill(10)
        try:
            archive = zipfile.ZipFile(data_dir+i[0]+'.zip')
            # print(archive)
        except:
            print('zip file corrupted: ', i[0])
            corrupted.append(i[0])
            # project_count += 1
            continue
        # print(project)
        image_count = 0
        for j in range(start_frame, end_frame+1):
            image_name = 'rgb/' + str(j).zfill(10) + '.png'         
            try:                
                with archive.open(image_name) as file:
                    image = Image.open(file)
                    # image = fn.resize(image, size=[224,224])
                    image.save(img_dir + 'img_' + str(image_count).zfill(5) + '.jpg', 'jpeg')
                    image_count += 1
            except:
                print('image corrupted: ', image_name)
                print('from: ', project, header)
                corrupted.append(project + ' ' +  header + ' ' + image_name)
                shutil.rmtree(img_dir)
                break      
            # project_count += 1
                
        # for file in archive.namelist():
        #     # print(file)
        #     if file.startswith('rgb/') and file.endswith('.png'):
        #         # print('file: ', file)
        #         num = file.strip('rgb/.png')
        #         # if num == '':
        #         #     continue
        #         # print(num)
        #         num = int(num)
        #         # print(num)
        #         # print(file)
        #         # print('start: ', start_frame)
        #         # print('end: ', end_frame)
        #         if num >= start_frame and num <= end_frame:
        #             # print(num)
        #             try:
        #                 image = Image.open(file)                
        #                 image = fn.resize(image, size=[224,224])
        #                 image.save(action_dir + 'img_' + str(image_count).zfill(5) + '.png')
        #                 # with open(img_dir + 'img_' + str(image_count).zfill(5) + '.png', 'wb') as f:
        #                     # f.write(archive.read(file))
        #                 image_count += 1
        #             except:
        #                 print('image corrupted: ', file)
        #                 corrupted.append(i[0])
        #                 project_count += 1
        #                 break
        #             # archive.extract(file, img_dir + 'img_' + str(image_count).zfill(5) + '.png')
        #         # count += 1
        #         # if file == start_frame:
        # project_count += 1
                # archive.extract(file, 'img_')

    corrupted = list(set(corrupted))           
    with open(image_dir + 'corrupted.txt', 'w') as f:
        for i in corrupted:
            f.write(i+'\n')
    # print(count)



def create_list(dir, num, labels):
    with open(dir+'pg_sp' + str(num) + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['clip', 'header', 'total_frame', 'action'])
        for i in labels:
            # clip = i[0]
            # header = i[1]
            total_frame = i[3] - i[2]
            data = [i[0]] + [i[4]] + [total_frame] + [i[1]]
            writer.writerow(data)  

# def create_list(csv):
#     with open(dir+'pg_sp' + str(num) + '.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['clip', 'header', 'total_frame', 'action'])
#         for i in labels:
#             # clip = i[0]
#             # header = i[1]
#             total_frame = i[3] - i[2]
#             data = [i[0]] + [i[4]] + [total_frame] + [i[1]]
#             writer.writerow(data)    

create_directory(image_dir)
# i = 0
# for i in range(len(file_names)):
for i in range(5):
    df = pd.read_csv(file_names[i], usecols=['Project','Action','Imgs'])
    label = create_label(df)
    create_list(save_dir, i, label)
    # create_data(label)
# print(labels[:5])
# create_list(save_dir, label)
# for i in labels:
#     print(i[0])
# print(len(labels))
