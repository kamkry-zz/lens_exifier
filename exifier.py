# A simple reader for EXIF metadata from JPEG files
# That was created to help with decision on which focal length
# was used by me more often -- so what should be focal length of
# mu next lens I'm planning to buy :)

# Created by Kamil Krysiak <kamkry18@gmail.com>
# on 02.I.2021 | v 1.0

import tkinter as tk        # library that contains go-to implementations for selecting files/directories
from tkinter import filedialog

import re
import exifread         # Cool library helping all things EXIF-related; more info on https://github.com/ianare/exif-py
# Copyright (c) 2002-2007 Gene Cash
# Copyright (c) 2007-2020 Ianaré Sévi and contributors

root = tk.Tk()
root.withdraw()

dir_path = filedialog.askopenfilenames()
#print(dir_path)

#file = open("c:/DSC_1441.jpg", 'rb')

iso_list = []
f_list = []
focal_list = []
shutter_list = []


def aperture_calc(exif_fnumber):       # As f-number value is represented as math operation, some treatment is needed
    item = str(exif_fnumber)
    item = item.split('/')

    if len(item) > 1:
        f_value = int(item[0])/int(item[1])
    else:
        if str(item[0]) == 'None':
            f_value = str(item[0])
        else:
            f_value = int(item[0])
    return f_value


def focal_calc(exif_focal_length):
    item = str(exif_focal_length)
    item = item.split('/')

    if len(item) > 1:
        focal_value = int(item[0]) / int(item[1])
    else:
        if str(item[0]) == 'None':
            focal_value = int(0)
        else:
            focal_value = int(item[0])
    return focal_value


def iso_calc(exif_iso):
    item = str(exif_iso)
    item = item.split('/')

    if len(item) > 1:
        iso_value = int(item[0]) / int(item[1])
    else:
        iso_value = int(item[0])
    return iso_value


def histogrammer(data_set_arg):
    data_list = []
    data_classes = set(data_set_arg)
    data_classes_number = len(data_classes)

    tmp = set(data_set_arg)
    histogram_data = {}
    for each_focal_length in tmp:
        histogram_data[each_focal_length] = data_set_arg.count(each_focal_length)
    return histogram_data

for file in dir_path:
    file = open(file, 'rb')
    tags = exifread.process_file(file, details=False)

    shutter_speed = str(tags.get('EXIF ExposureTime'))
    shutter_speed = re.split('=', shutter_speed)

    focal_length = tags.get('EXIF FocalLength')
    focal_length = focal_calc(focal_length)

    iso = tags.get('EXIF ISOSpeedRatings')
    iso = iso_calc(iso)

    aperture = tags.get('EXIF FNumber')
    aperture = aperture_calc(aperture)

    iso_list.append(iso)
    f_list.append(aperture)
    focal_list.append(focal_length)
    shutter_list.append(shutter_speed[0])


def grapher(data):

    every_class = list(data.keys())
    #every_class = every_class.
    every_class = sorted(every_class)
    print("======================================")
    print()
    for bin in range(0,len(every_class)):
        print(every_class[bin],"mm", end='')
        key = every_class[bin]
        value = data[key]
        bar = value*"#"
        print(" | ",value, " ",bar )
        if str(every_class[bin]) == 'None':
            pass
    print()
    return




print()
#print("Shutter speed:",shutter_list)
#print("Focal length:", focal_list)
#print("F-number:", f_list)
#print("ISO:", iso_list)

print('HISTOGRAM:', histogrammer(focal_list))
print(grapher(histogrammer(focal_list)))
print("TOTAL number of photos:",len(focal_list))



