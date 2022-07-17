import time
from string import printable
import sympy
import ast
import requests
import codecs
import sympy
import re
from sympy.parsing.latex import parse_latex
from bs4 import BeautifulSoup
from typing import List
import fitz
from fitz.fitz import Point, Page, Rect
from pprint import pprint
from itertools import groupby
import json
import skimage
from difflib import SequenceMatcher

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage.color import rgb2gray
from skimage.morphology import (erosion, dilation, closing, opening,
                                area_closing, area_opening)
from skimage.measure import label, regionprops, regionprops_table

from pdf2image import convert_from_path

print(SequenceMatcher(None, 'abcd', 'abce').ratio())

# optional
# import pdfkit

# print(fitz.__doc__)

#BASE_PATH = "/home/bernardo/Scaricati"
DOC_NAME = "Tkaczyk2015_Article_CERMINEAutomaticExtractionOfSt.pdf"
# DOC_NAME = "Cheng2020_Chapter_MaximumEntropyRegularizationAn.pdf"
# DOC_NAME = "Zhou2020_Chapter_AnImprovedConvolutionalBlockAt.pdf"
# DOC_NAME = "Das-Jawahar2020_Chapter_AdaptingOCRWithLimitedSupervis.pdf"
# DOC_NAME = "Chakraborty2022_Article_ModelingRight-skewedHeavy-tail.pdf"
#DOC_PATH = BASE_PATH + "/" + DOC_NAME
#doc = fitz.open(f"{DOC_PATH}")
# apri pure più pagine oltre la prima

from fitz.utils import getColorList

cl = getColorList()
print(cl)
color_line = fitz.utils.getColor("BLUE")
color_rect = fitz.utils.getColor("ORANGE")
color_bezr = fitz.utils.getColor("BROWN")
color_block = fitz.utils.getColor("RED")
color_textline = fitz.utils.getColor("PURPLE")
color_word = fitz.utils.getColor("YELLOW1")
color_references = fitz.utils.getColor("GREEN")
color_images = fitz.utils.getColor("AQUAMARINE")
color_fig_caption = fitz.utils.getColor("YELLOW3")
color_Tab_caption = fitz.utils.getColor("DARKBLUE")
color_white = fitz.utils.getColor("WHITE")
# %%
# immagini


def find_image(BASE_PATH, DOC_NAME,PDF_directory, Output_directory, idx, fig_caption_coords, color_white, color_images):
    DOC_PATH = BASE_PATH + "/" + PDF_directory + "/" + DOC_NAME
    doc = fitz.open(f"{DOC_PATH}")
    index = 0
    for page2 in doc:
        eq_bbox = [0, 0, 0, 0]
        #index += 1
        if index > idx:
            break
        if index > idx-1:
            page3 = page2
            images = page2.get_image_info()
            print("images: " + str(images))
            texts = page2.get_text("json")
            texts = json.loads(texts)
            line = False
            print("len(texts['blocks']): " + str(len(texts['blocks'])))
            # page2.draw_rect(Rect([170, 125, 150, 150]), color=color_rect)
            for block in texts['blocks']:
                # page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
                s = ""
                colored = False
                try:
                    print(block['lines'][0]['spans'][0]['text'])
                    line = True
                except:
                    line = False
                    print("Error")
                if line is True:
                    if block['type'] == 0:
                        page2.draw_rect(Rect(block['bbox']), color=color_white, width=1.5, fill=color_white)
                if block['type'] == 1:  # images
                    page2.draw_rect(Rect(block['bbox']), color=color_white, width=1.5, fill=color_white)
        index+=1
    lenght = len(doc)
    if idx == 0:
        doc.delete_pages(1, len(doc) - 1)
    elif idx == 1:
        doc.delete_page(0)
        doc.delete_pages(1, len(doc) - 1)
    elif idx == 2:
        doc.delete_pages(0, 1)
        doc.delete_pages(1, len(doc) - 1)
    elif idx == len(doc)-2:
        doc.delete_pages(0, len(doc)-3)
        doc.delete_page(1)
    elif idx==len(doc)-1:
        doc.delete_pages(0, len(doc)-2)
    else:
        doc.delete_pages(0, idx-1)
        doc.delete_pages(1, len(doc) - 1)
    doc.save(f'{BASE_PATH}/'+PDF_directory+ "/" + DOC_NAME.replace(".pdf", "") + '_3.pdf')


    pages = convert_from_path(f'{BASE_PATH}/' + PDF_directory + "/" + DOC_NAME.replace(".pdf", "") + '_3.pdf', 500)

    for page in pages:
        page.save(f'{BASE_PATH}/' + PDF_directory + "/" + DOC_NAME.replace(".pdf", "") + '_3.jpg', 'JPEG')

    painting = plt.imread(f'{BASE_PATH}/' + PDF_directory + "/" + DOC_NAME.replace(".pdf", "") + '_3.jpg')
    plt.imshow(painting, vmin=0, vmax=255)
    plt.show()
    gray_painting = rgb2gray(painting)
    # binarized = gray_painting < 0.55
    binarized = gray_painting < 0.60
    imshow(binarized)
    plt.show()

    square = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])

    def multi_dil(im, num, element=square):
        for i in range(num):
            im = dilation(im, element)
        return im

    def multi_ero(im, num, element=square):
        for i in range(num):
            im = erosion(im, element)
        return im

    multi_dilated = multi_dil(binarized, 7)
    area_closed = area_closing(multi_dilated, 50000)
    multi_eroded = multi_ero(area_closed, 7)
    opened = opening(multi_eroded)
    imshow(opened)
    plt.show()

    label_im = label(opened)
    regions = regionprops(label_im)
    imshow(label_im)
    plt.show()

    properties = ['area', 'convex_area', 'bbox_area', 'extent',
                  'mean_intensity', 'solidity', 'eccentricity',
                  'orientation', 'bbox']
    df = pd.DataFrame(regionprops_table(label_im, gray_painting,
                                        properties=properties))
    print(df)

    masks = []
    bbox = []
    list_of_index = []
    for num, x in enumerate(regions):
        area = x.area
        convex_area = x.convex_area
#        if (num != 0 and (area > 100) and (convex_area / area < 1.05)
#                and (convex_area / area > 0.95)):
        if (area > 50):
            masks.append(regions[num].convex_image)
            bbox.append(regions[num].bbox)
            list_of_index.append(num)
    count = len(masks)
    if count.__eq__(0):
        return [0, 0, 0, 0]
    if count.__eq__(1):
        fig, ax = plt.subplots(2, count, figsize=(15, 8))
        for axis, box, mask in zip(ax.flatten(), bbox, masks):
            red = painting[:, :, 0][box[0]:box[2], box[1]:box[3]] * mask
            green = painting[:, :, 1][box[0]:box[2], box[1]:box[3]] * mask
            blue = painting[:, :, 2][box[0]:box[2], box[1]:box[3]] * mask
            image = np.dstack([red, green, blue])
            axis.imshow(image)
        plt.show()
    else:
        fig, ax = plt.subplots(2, int(count / 2), figsize=(15, 8))
        for axis, box, mask in zip(ax.flatten(), bbox, masks):
            red = painting[:, :, 0][box[0]:box[2], box[1]:box[3]] * mask
            green = painting[:, :, 1][box[0]:box[2], box[1]:box[3]] * mask
            blue = painting[:, :, 2][box[0]:box[2], box[1]:box[3]] * mask
            image = np.dstack([red, green, blue])
            axis.imshow(image)
        plt.show()

    rgb_mask = np.zeros_like(label_im)
    for x in list_of_index:
        rgb_mask += (label_im == x + 1).astype(int)
    red = painting[:, :, 0] * rgb_mask
    green = painting[:, :, 1] * rgb_mask
    blue = painting[:, :, 2] * rgb_mask
    image = np.dstack([red, green, blue])
    imshow(image)
    plt.show()

    centroids = []
    import math
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)
    box1 = [0, 0, 0, 0]
    for props in regions:
        y0, x0 = props.centroid
        if props.area > 75 and (props.axis_minor_length/props.axis_major_length) > 0.1:
            print("props.bbox[0]: "+str(props))
            centroids.append(props.centroid)
            print("x0 e y0: " + str(x0) + ", " + str(y0))
            orientation = props.orientation
            x1 = x0 + math.cos(orientation) * 0.5 * props.minor_axis_length
            y1 = y0 - math.sin(orientation) * 0.5 * props.minor_axis_length
            x2 = x0 - math.sin(orientation) * 0.5 * props.major_axis_length
            y2 = y0 - math.cos(orientation) * 0.5 * props.major_axis_length

            # ax.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
            # ax.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
            ax.plot(x0, y0, '.g', markersize=15)

            minr, minc, maxr, maxc = props.bbox
            if box1[0] == 0:
                box1[0] = minc
            if box1[1] == 0:
                box1[1] = maxc
            if box1[2] == 0:
                box1[2] = minr
            if box1[3] == 0:
                box1[3] = maxr
            if box1[0] > minc:
                box1[0] = minc
            if box1[1] < maxc:
                box1[1] = maxc
            if box1[2] > minr:
                box1[2] = minr
            if box1[3] < maxr:
                box1[3] = maxr
            # bx = (minc, maxc, maxc, minc, minc)
            # by = (minr, minr, maxr, maxr, minr)
            # ax.plot(bx, by, '-b', linewidth=2.5)
    bx = (box1[0], box1[1], box1[1], box1[0], box1[0])
    by = (box1[2], box1[2], box1[3], box1[3], box1[2])
    ax.plot(bx, by, '-b', linewidth=2.5)

    # ax.axis((0, 3000, 5000, 0))
    plt.show()
    fig = plt.figure()
    bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width * fig.dpi, bbox.height * fig.dpi

    DOC_NAME2 = DOC_NAME.replace(".pdf", "")+"_3.pdf"
    DOC_PATH2 = BASE_PATH + "/" + PDF_directory + "/"  + DOC_NAME2

    doc2 = fitz.open(f"{DOC_PATH2}")
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0
    box_image = [0, 0, 0, 0]
    for page2 in doc2:
        print("box1: " + str(box1))
        print(page2.mediabox)
        print(image.shape)
        xmin = box1[0] * page2.mediabox[2] // image.shape[1]
        xmax = box1[1] * page2.mediabox[2] // image.shape[1]
        ymin = box1[2] * page2.mediabox[3] // image.shape[0]
        ymax = box1[3] * page2.mediabox[3] // image.shape[0]
        page2.draw_rect(Rect([xmin, ymin, xmax, ymax]), color=color_images)
        # page2.draw_rect(Rect([100,200,300,400]), color=color_block)
    box_image[0] = xmin
    box_image[1] = ymin
    box_image[2] = xmax
    box_image[3] = ymax
    doc2.save(f'{BASE_PATH}/' + PDF_directory + "/" + DOC_NAME2.replace("_3.pdf", "") + '_4.pdf')
    return box_image

# find_image(BASE_PATH, DOC_NAME, 11, color_white, color_images)
# find_image(BASE_PATH, DOC_NAME, 8, color_white, color_images)
# find_image(BASE_PATH, DOC_NAME, 13, color_white, color_images)