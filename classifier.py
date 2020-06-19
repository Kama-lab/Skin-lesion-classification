import keras
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import cv2
from keras.models import load_model,model_from_json
import csv
import copy
import xlsxwriter
from PyQt5.QtGui import QImage
from shutil import copyfile

labels = ['Actinic Keratoses', 'Basal cell carcinoma', 'Benign keratosis', 'Dermatoﬁbroma', 'Melanoma', 'Melanocytic nev', 'Vascular skin lesions']
models = {"MobileNet":["MobileNet_model.json","MobileNet_weights.h5"],
          "Xception":["Xception_model.json","Xception_weights.h5"],
          "InceptionV3":["InceptionV3_model.json","InceptionV3_weights.h5"],
          "InceptionResNet":["InceptionResNetV2_model.json","InceptionResNetV2_weights.h5"],
          "C128":["C128_model.json","C128_weights.h5"],
          }

images = {}

def predict_image(image_name,selected_model):

    name,weights = models[selected_model]
    
    model_json = open("models/"+name,"r")
    load = model_json.read()
    model_json.close()
    model = model_from_json(load)

    model.load_weights("weights/"+weights)


    _,w,h,ch = model.layers[0].input.shape


    img = cv2.imread(images[image_name][0])
    img = cv2.resize(img,(w,h))
    q_image = np_to_qImage(img)
    img = np.reshape(img,[1,w,h,ch])
    img = img.astype("float32")
    img /= 255

    probabilities = model.predict(img)

    results = {}
    n=0
    for i in labels:
        results[i] = float("%.2f" % (probabilities[0][n]*100))
        n+=1
    images[image_name][4] = q_image
    images[image_name][3] = f"{w}x{h}"
    images[image_name][2] = results
    
    return results


def np_to_qImage(img):
    height, width, channel = img.shape
    bytes_per_line = 3 * width
    image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
    return image


def predict_images(images,model):
    for i in images:
        prob = predict_image(i,model)
    return prob 
    

def retrieve_name_from_path(file,ext_length):
    i=-1
    raw_name = ""
    while(True):
        if file[i] == '/' or file[i] == '\\':
            break
        raw_name += file[i]
        i-=1
    raw_name = raw_name[:ext_length:-1]
    return raw_name

def add_image(image_file):
    raw_name = retrieve_name_from_path(image_file,3)
    ext_name = image_file[::-1]
    if ext_name[3::-1] == ".jpg" or ext_name[3::-1] == ".jpeg":
        images[raw_name] = [image_file,find_image_size(image_file),False,"",""]
    else:
        raw_name = False
    return raw_name


def find_image_size(image_file):
    image = cv2.imread(image_file)
    dimensions = image.shape
    return f"{dimensions[1]}x{dimensions[0]}"

def get_image_info(image_name):
    return images[image_name]

def get_models():
    return models
    

def save(file,ext):
    buffer_file = []
    column_labels = copy.deepcopy(labels)
    column_labels.insert(0,"Name")
    column_labels.insert(1,"Location")
    buffer_file.append(column_labels)

    for i in images:
        row = []
        if(images[i][2]):
            row.append(f"{i}.jpg")
            row.append(f"{images[i][0]}")
            [row.append(n) for n in images[i][2].values()]
        buffer_file.append(row)
    try:
        if ext=="csv":
            with open(file[0],"w",encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerows(buffer_file)
        else:
            wb = xlsxwriter.Workbook(file[0])
            ws = wb.add_worksheet()
            for row in range(len(buffer_file)):
                for col in range(len(buffer_file[row])):
                    ws.write(row,col,buffer_file[row][col])
            wb.close()
    except Exception as error:
        raise FileNotFoundError

def add_model(model_path,weights_path,name):

    errorOccured = 0

    model_name = retrieve_name_from_path(model_path,0)
    weights_name = retrieve_name_from_path(weights_path,0)

    copyfile(model_path,'models/'+model_name)
    copyfile(weights_path,'weights/'+weights_name)
    try:
        model_json = open("models/"+model_name,"r")
        load = model_json.read()
        model_json.close()
        model = model_from_json(load)
    except:
        errorOccured = "Model can not be compiled!"
    try:
        model.load_weights("weights/"+weights_name)
    except:
        errorOccured = "Weights can not be loaded into model!"
    try:
        _,w,h,ch = model.layers[0].input.shape
    except:
        errorOccured = "Model input shape is unknown!"

    if errorOccured == 0:
        models[str(name)] = [model_name,weights_name]
    return errorOccured

