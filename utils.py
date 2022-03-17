import os
import pandas as pd
import csv

clips = {'minsung': ['20210923_155848', '20210923_161107'], 'priya': ['20210923_163035', '20210923_163801'], 'fadl': ['20211001_152746', '20211001_154310']}

# pg_corrupted = ['']

# merge actions to be less
merge_acts_9classNother = {
    'chewing':'chewing', 
    'no action':'no action',
    'move hand away from mouth':'move hand away from mouth',
    'move hand towards mouth':'move hand towards mouth',
    'pick food from utensil with both hands':'pick food from utensil with both hands',
    'pick food from utensil with one hand':'pick food from utensil with one hand', 
    'eat it':'eat it',
    'pick food from utensil with tool in one hand':'pick food from utensil with tool in one hand', 
    'pick food from utensil with tools in both hands': 'pick food from utensil with tools in both hands',
    'crop action':'ignore',
    'other activity':'other', 
    'wipe mouth with hand':'other', 
    'put/spread on':'other', 
    'clean mouth/hands':'other', 
    'pick up a napkin/tissue':'other', 
    'put the napkin/tissue back':'other', 
    'did not put the cup/glass back':'other', 
    'pick up a jar/box':'other', 
    'open the jar/box':'other', 
    'close the jar/box':'other', 
    'put the jar/box back':'other', 
    'mixing':'other',  
    'take out from the box':'other', 
    'did not put the food back':'other',
    'sitting down - start activity':'other',
    'finish food - end activity':'other',
    'finish food':'other',
    'pick up a cup/glass':'other', 
    'put the cup/glass back':'other',
    'pick up no tool':'other', 
    'put the food back':'other', 
    'put one tool back':'other',
    'pick up a tool with one hand':'other', 
    'pick up tools with both hands':'other', 
    'put both tools back':'other',
    'food in hand at table':'other', 
    'drink':'other'
    }

# merged actions
Actions_10 = {'other': 0, 'pick food from utensil with both hands': 1, 'pick food from utensil with one hand': 2, 'move hand towards mouth': 3, 'eat it': 4, 'move hand away from mouth': 5, 'chewing': 6, 'no action': 7, 'pick food from utensil with tools in both hands': 8, 'pick food from utensil with tool in one hand': 9}


def create_directory(dir_name):
    # Create target Directory if don't exist
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        # print("Directory " , dir_name ,  " Created ")
    else:    
        print("Directory " , dir_name ,  " already exists")


# pg_colab_dir = '/content/datasets/ug_data/'
# rawframe annotation
# def create_rawframe_annot(colab_dir, ):
#     # 5 fold train and valid
#     for i in range(5):
#         train = [*range(0,5)]
#         val = i
#         train.remove(i)
#         with open(label_dir+'train_'+'sp'+str(i)+'.txt', 'w', newline='') as f:
#             for j in train:
#                 for k in sp[j]:
#                     clip, total_frame, action_num = data_all[k]
#                     # print(clip, total_frame, action)
#                     data = data_colab_dir + k + ' ' + str(total_frame) + ' ' + str(action_num) + '\n'
#                     # print(data)
#                     f.write(data)
#         with open(label_dir+'val_'+'sp'+str(i)+'.txt', 'w', newline='') as f:
#             for l in sp[i]:
#                 clip, total_frame, action_num = data_all[l]
#                 # print(clip, total_frame, action)
#                 data = data_colab_dir + l + ' ' + str(total_frame) + ' ' + str(action_num) + '\n'
#                 # print(data)
#                 f.write(data)

