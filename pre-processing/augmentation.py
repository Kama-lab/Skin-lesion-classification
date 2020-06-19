import os
import shutil
import keras
import numpy as np


# we are not augmenting the biggest class of 'nv'
class_list = ['mel','bkl','bcc','akiec','vasc','df']
for item in class_list:
     
    aug_dir = 'aug_dir'
    os.mkdir(aug_dir)
    img_dir = os.path.join(aug_dir, 'img_dir')
    os.mkdir(img_dir)
    img_class = item
    img_list = os.listdir('train/' + img_class)
    for fname in img_list:
        shutil.copyfile(
            os.path.join('train/' + img_class, fname), 
            os.path.join(img_dir, fname))
    datagen = keras.preprocessing.image.ImageDataGenerator(
        rotation_range=180,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest')
    batch_size = 50
     
    aug_datagen = datagen.flow_from_directory(
        'aug_dir',
        save_to_dir='train/' + img_class,
        save_format='jpg',
        target_size=(224,224),
        batch_size=batch_size)
    num_aug_images_wanted = 6000 
     
    num_files = len(os.listdir(img_dir))
    num_batches = int(np.ceil((num_aug_images_wanted-num_files)/batch_size))
    for i in range(0,num_batches):
        imgs, labels = next(aug_datagen)
         
    shutil.rmtree('aug_dir')
     
print(str(len(os.listdir('train/nv'))) + ' in nv dir')
print(str(len(os.listdir('train/mel'))) + ' in mel dir')
print(str(len(os.listdir('train/bkl'))) + ' in bkl dir')
print(str(len(os.listdir('train/bcc'))) + ' in bcc dir')
print(str(len(os.listdir('train/akiec'))) + ' in akiec dir')
print(str(len(os.listdir('train/vasc'))) + ' in vasc dir')
print(str(len(os.listdir('train/df'))) + ' in df dir')
