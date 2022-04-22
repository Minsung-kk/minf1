import csv
from venv import create
import utils
import pandas as pd
import zipfile
import math
import torchvision
import json
import torchvision.transforms.functional as fn
import torchvision.transforms as tf
from torchvision import datasets
from sklearn.model_selection import KFold
from PIL import Image

# data locations
data_dir = '/Users/minsungkim/Downloads/datasets/'
colab_data_dir = '/content/datasets/'

# file name and clips for each person
clips = {'minsung': ['20210923_155848', '20210923_161107'], 'priya': ['20210923_163035', '20210923_163801'], 'fadl': ['20211001_152746', '20211001_154310']}
# minsung = {'file': 'minsung', 'clips': }
# priya = {'file': 'priya', 'clips':['20210923_163035', '20210923_163801']}
# fadl = {'file': 'fadl', 'clips':[]}

# frame rate for clips
frame_rate = 15

# for i in files:
    # df = pd.read_csv(i, usecols=['Project','Action','Imgs'])
# test = data+minsung_clips[1]+'.csv'

# center crop - replaced by torchvision.transforms
# def center_crop(image):
#     im = Image.open(image)
#     width, height = im.size   # Get dimensions
#     new_width = 280
#     new_height = 320
#     left = (width - new_width)/2
#     top = (height - new_height+150)/2
#     right = (width + new_width)/2
#     bottom = (height + new_height+50)/2
#     # Crop the center of the image
#     return im.crop((left, top, right, bottom))

# convert seconds to frame
def seconds_to_frame(frame_rate, start, end):
    start_frame = int(round(float(start*frame_rate)))
    end_frame = int(round(float(end*frame_rate)))
    total_frame = end_frame - start_frame + 1
    return start_frame, end_frame, total_frame

# create labels to sort images and write annotations
def create_label(clip):
    labels = []
    csv = data_dir+clip+'.csv'
    df = pd.read_csv(csv)
    count = 0
    # print(i)
    # skip the first line
    for index, row in df.iloc[1:].iterrows():
        # index[0]: header
        # index[2]: temporal segment start
        # index[3]: temporal segment end
        # row[0][20:-2]: metadata(activity)
        # check whether temporal segments and actions are valid
        header = index[0]
        start = float(index[2])
        end = float(index[3])
        if math.isnan(start) or math.isnan(end) or len(row[0][20:-2])<4:                
            continue
        # merge actions to 9 actions and other
        action = utils.merge_acts_9classNother[row[0][20:-2]]
        # action number
        action_num = utils.Actions_10[action]
        # get start frame and end frame to gather images, 
        # and total frame for annotation
        # convert frames to float
        start_frame, end_frame, total_frame = seconds_to_frame(
            frame_rate, start, end)
        if total_frame < frame_rate/2:
        # total_frame > 1000/frame_rate:
            continue
        #     print('yay')
        # print(total_frame)
        label = [clip, header, start_frame, end_frame, total_frame, action, action_num]
        labels.append(label)
    return labels

# create labels from json file
def create_label_json(clip):
    labels = []
    # file location
    file = open(data_dir + clip + '.json')
    # load json objects from the file
    jsonObject = json.load(file)
    # get metadata including time stamps and actions
    jsonArray = jsonObject.get("metadata")
    # write the annotation file
    for i in jsonArray.keys():
        
        # get an action for the current key
        pre_action = jsonArray.get(i).get("av").get("1")
        
        # print('before: ', action)
        # merge the action by returning the value from mergeacts
        action = utils.merge_acts_9classNother.get(pre_action)
        
        # use the action if mergeacts do not have the key 'action'
        if action == None:
            action = pre_action
        action_num = utils.Actions_10[action]
        # get a time stamp
        interval = jsonArray.get(i).get('z')
        if len(interval) < 2:
            continue
        start, end = interval
        start_frame, end_frame, total_frame = seconds_to_frame(
            frame_rate, start, end)
        # only retrieve values if they have a starting point and an end point for debugging
        # if len(interval) > 1:
            # labels[mergedAction].append(i)
            # intervals[i]=interval
            # frameToVideo(i, interval)
            # videoLabel(i, videoType, mergedAction)
        label = [clip, i, start_frame, end_frame, total_frame, action, action_num]
        labels.append(label)
    return labels

# count how many each action happend
def count_actions(labels):
    count = {}
    for i in labels:
        action = i[5]
        num = str(action)
        try:
            count[num] += 1
        except:
            count[num] = 1
    return dict(sorted(count.items(), key=lambda item: item[0]))

# to specify where headers belong to a person
def create_list(labels):
    with open(data_dir+'ug_list.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['clip', 'header','action'])
        for i in labels:
            # clip = i[0]
            # header = i[1]
            data = i[:2] + [i[6]]
            writer.writerow(data)           

# sort images by frames
def frames_to_images(dir, file_name, labels):
    # check the zip file is valid
    try:
        archive = zipfile.ZipFile(dir+file_name)
    except:
        print('zip file corrupted: ', file_name)
    # dir for the clip
    image_data_dir = dir + labels[0][0] + '/'
    utils.create_directory(image_data_dir)
    # find images correspond to actions, and save them
    for i in labels:
        # make a directory for an action
        action_dir = image_data_dir + i[1] + '/'
        utils.create_directory(action_dir)
        # image number
        image_count = 0
        # from start frame to end frame
        for j in range(i[2], i[3]):
            image_name = i[0] + '/rgb/' + str(j).zfill(10) + '.png'
            with archive.open(image_name) as file:
                # image = center_crop(file)
            # image = center_crop(image_name)  
                try:
                    image = Image.open(file)
                    # image = fn.resize(image, size=[224,224])
                    image.save(action_dir + 'img_' + str(image_count).zfill(5) + '.jpg', 'jpeg')
                    # with open(action_dir + 'img_' + str(image_count).zfill(5) + '.png', 'wb') as f:
                    #     f.write(image)
                        # f.write(center_crop(action_dir + 'img_' + str(image_count).zfill(5) + '.png'))
                    image_count += 1
                except:
                    print('image corrupted: ', image)
                    # corrupted.append(i[0])
                    # project_count += 1
                    break

def create_annotation(dir, labels):
    with open(dir +  + '.txt', 'w') as f:
        for i in labels:
            f.write(dir+i[0])

# print(count_actions(create_label_json(clips['fadl'][0])))
# print(count_actions(create_label(clips['minsung'][0])))
# print(count_actions(create_label(clips['minsung'][1])))


# labels = create_label(clips['minsung'][0]) 
# print(labels[:4])
# frames_to_images(data_dir, 'minsung.zip', labels)
# create_list(labels, 'minsung')
total_labels = []
for i in clips['minsung']:
    labels = create_label(i)
    # frames_to_images(data_dir, 'minsung.zip', labels)
    total_labels.extend(labels)
for i in clips['priya']:
    labels = create_label(i)
    total_labels.extend(labels)
    # frames_to_images(data_dir, 'priya.zip', labels)
for i in clips['fadl']:
    labels = create_label_json(i)
    total_labels.extend(labels)
    # frames_to_images(data_dir, 'fadl.zip', labels)
    
# create_list(total_labels)
    

# print(create_label_json(clips['fadl'][1]))
# for i in clips.items():
#     print(i)

# labels = []
# for i in clips['priya']:
#     labels.extend(create_label(i))
# print(labels)
# create_list(labels)

# dataset = datasets.ImageFolder(data_dir)
# for i in dataset:
#     i.
# print(dataset)

# center_crop(
path = '/Users/minsungkim/Downloads/datasets/20210923_155848/1_6S9uj0A6/img_00000.png'
sample_path = '/Volumes/ETC/MInf/20210606_154234.zip'

archive = zipfile.ZipFile(sample_path)
image_name = 'rgb/' + str(0).zfill(10) + '.png'
# '/20210606_154234' + '/rgb/' + str(0).zfill(10) + '.png'

# for i in archive.namelist():
#     print(i)

# with archive.open(image_name) as file:
#     img = Image.open(file)
#     # print("This is size of original image:",img.size, "\n")
#     resize = fn.resize(img, size=[224,224])
#     resize.show()
#     random_crop = tf.RandomResizedCrop(100)
#     crop_image = random_crop(img)
#     crop_image.show()
