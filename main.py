# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from string import printable
import sympy
import ast
import requests
import codecs
import os
import sympy
import re
from sympy.parsing.latex import parse_latex
from bs4 import BeautifulSoup

BASE_PATH = "/home/bernardo/Scaricati"
print("Insert Link: ")
link = input()
print("Link is: "+link)
# link = "https://link.springer.com/article/10.1007/s10032-015-0249-8"
# link = "https://link.springer.com/chapter/10.1007/978-3-030-57058-3_1"
# link = "https://link.springer.com/chapter/10.1007/978-3-030-57058-3_2"
# link = "https://link.springer.com/chapter/10.1007/978-3-030-57058-3_3"
# link = "https://link.springer.com/article/10.1007/s10032-019-00317-0"
# link = "https://link.springer.com/article/10.1007/s10032-018-0312-3"
#link = "https://link.springer.com/article/10.1007/s40840-022-01317-w"
#link = "https://link.springer.com/article/10.1134/S2070048222040093"
with requests.Session() as s:
    s.proxies = {'https': 'http://7036865:Tbernardo96@proxyunifi.unifi.it:8888'}

    response_link = s.post(link)
    r_link = s.get(link)
    soup1 = BeautifulSoup(r_link.text, "html.parser")
    title_link = soup1.find('title').text

    print(title_link)
    path_to_html_file = BASE_PATH+"/"+title_link+".html"
    print(path_to_html_file)
    file_exists = os.path.exists(path_to_html_file)
    if not file_exists:
        with open(path_to_html_file, 'wb') as f3:
            print('html page download')
            f3.write(r_link.content)
    else:
        print('html page exists')
    pdf_url = soup1.find("meta", attrs={"name": "citation_pdf_url"})['content']
    print(pdf_url)
    response = s.post(pdf_url)
    #print(response)
    r = s.get(pdf_url)
    print(":"+r.headers['content-disposition'].replace("inline; filename=", ""))
    pdf_name = r.headers['content-disposition'].replace("inline; filename=", "")
    path_to_pdf_file = BASE_PATH+"/"+r.headers['content-disposition'].replace("inline; filename=", "")
    pdf_exists = os.path.exists(path_to_pdf_file)
    if not pdf_exists:
        print('pdf download')
        with open(path_to_pdf_file, 'wb') as f3:
            f3.write(r.content)
    else:
        print('pdf exists')
    #exit(0)

f = codecs.open(path_to_html_file)
# f = codecs.open("/home/bernardo/Scaricati/CERMINE automatic extraction of structured metadata from scientific literature | SpringerLink.html", "r")
#f = codecs.open(
#    "/home/bernardo/Scaricati/Maximum Entropy Regularization and Chinese Text Recognition | SpringerLink.html", "r")
#f = codecs.open(
#    "/home/bernardo/Scaricati/An Improved Convolutional Block Attention Module for Chinese Character Recognition | SpringerLink.html", "r")
# f=codecs.open("/home/bernardo/Scaricati/Adapting OCR with Limited Supervision | SpringerLink.html")
# f=codecs.open("/home/bernardo/Scaricati/Modeling Right-skewed Heavy-tail Right-censored Survival Data with Application to HIV Viral Load | SpringerLink.html")
page = f

soup = BeautifulSoup(f.read(), 'html.parser')
#print(soup.prettify())
print("\nOIOIOIO\n")

print([type(item) for item in list(soup.children)])
print(soup.find_all(name='dc.description'))
print(soup.find_all('script', class_='js-entry'))
html = list(soup.children)[2]
# print(list(html.children))

f1 = codecs.open(
    "/home/bernardo/Scaricati/KERTAS dataset for automatic dating of ancient Arabic manuscripts | SpringerLink.html",
    "r")
page1 = f1
soup1 = BeautifulSoup(f1.read(), 'html.parser')
print(soup1.find_all('h2', class_='c-article-section__title js-section-title js-c-reading-companion-sections-item'))
print(soup1.find_all('figcaption', class_='c-article-table__figcaption'))
print(soup1.find_all('div', class_='c-article-section__figure-description'))
L2 = soup1.find_all('div', class_='c-article-section__figure-description')
print(len(L2))

#print(soup1.find_all('div', class_='c-article-equation')[1])

#print(soup.find_all('div', class_='c-article-equation')[1])

l3 = soup.find_all('div', class_='c-article-section__figure-description')
l4 = soup1.find_all('figcaption', class_='c-article-table__figcaption')

print(len(l4))

l5 = []
for row in soup.find_all('h2', class_='c-article-section__title js-section-title js-c-reading-companion-sections-item'):
    l5.append(row.text)
print("l5: "+str(l5))
l6 = []
for row in soup.find_all('h3', class_=lambda value: value and value.startswith('c-article__sub-heading')):
    l6.append(row.text)
print("l6: " + str(l6))
l5 += l6
l7 = []
for row in soup.find_all('h4', class_=lambda value: value and value.startswith('c-article__sub-heading')):
    l7.append(row.text)
print("l7: " + str(l7))
l5 += l7
print("l5+l6+l7: "+str(l5))

title = []
for row in soup.find_all('h1', class_=lambda value: value and value.startswith('c-article-title')):
    title.append(row.text)
print("title: "+str(title))
l5 += title
print("l5+l6+l7+title: "+str(l5))

references=[]
for row in soup.find_all('p', class_=lambda value: value and value.startswith('c-article-references__text')):
    references.append(row.text)
print("references: "+str(references))
print(len(references))


from pylatexenc.latex2text import LatexNodes2Text
'''
l8 = []
number=0
for row in soup.find_all('script', type='math/tex; mode=display'):
    number += 1
    row2 = LatexNodes2Text().latex_to_text(row.text+"("+str(number)+")")
    l8.append(row2)
'''
l8 = []
number=0
for row in soup.find_all('div', class_='c-article-equation__content'):
    number += 1
    row2 = LatexNodes2Text().latex_to_text(row.text.replace("", "")+"("+str(number)+")")
    l8.append(row2)

print("l8: " + str(l8))
dictl8 = {i: l8[i] for i in range(0, len(l8))}
print("dictl8: " + str(dictl8))

figures_caption = []
for row in soup.find_all('div', class_=lambda value: value and value.startswith('c-article-section__figure js-c-reading-companion-figures-item')):
    figures_caption.append(row.text)
print("figure_caption: "+str(figures_caption))
tables_caption = []
for row in soup.find_all('figcaption', class_=lambda value: value and value.startswith('c-article-table__figcaption')):
    tables_caption.append(row.text)
print("table_caption: "+str(tables_caption))


def split(word):
    return [char for char in word]


def title_inner(title, block):
    finded = False
    box = [0, 0, 0, 0]
    for i in range(len([0])):
        line = ""
        for j in range(len(block['lines'][i]['spans'])):
            line += " " + block['lines'][i]['spans'][j]['text']
            print(block['lines'][i]['spans'][j]['text'].__contains__(title))
            if (title.__eq__(block['lines'][i]['spans'][j]['text']) or SequenceMatcher(None, block['lines'][i]['spans'][j]['text'].replace(" ", ""), title).ratio() >= 0.8)\
                    and (block['lines'][i]['spans'][j]['flags']==20 or block['lines'][i]['spans'][j]['flags']==6):
                finded = True
                box = block['lines'][i]['spans'][j]['bbox']
                break
            elif (title.__eq__(line)
                or line.__contains__(title) or SequenceMatcher(None, line.replace(" ", ""), title).ratio() >= 0.8)\
                    and ((block['lines'][i]['spans'][0]['flags']==20 and block['lines'][i]['spans'][len(block['lines'][i]['spans'])-1]['flags']==20) or
                         (block['lines'][i]['spans'][j]['flags']==6 and block['lines'][i]['spans'][len(block['lines'][i]['spans'])-1]['flags']==6)):
                box = block['lines'][i]['bbox']
                finded = True
                break
    return finded, box


def utils(eq_bbox, block):
    if eq_bbox[0] == 0 or eq_bbox[2] == 0:
        eq_bbox[0] = block['bbox'][0]
        eq_bbox[2] = block['bbox'][2]
    if eq_bbox[1] == 0 and eq_bbox[3] == 0:
        eq_bbox[1] = block['bbox'][1]
        eq_bbox[3] = block['bbox'][3]
    elif eq_bbox[1] <= block['bbox'][1] and block['bbox'][3] > eq_bbox[3] >= block['bbox'][1]:
        eq_bbox[3] = block['bbox'][3]
        if eq_bbox[0] > block['bbox'][0]:
            eq_bbox[0] = block['bbox'][0]
        if eq_bbox[2] < block['bbox'][2]:
            eq_bbox[2] = block['bbox'][2]
    elif eq_bbox[1] <= block['bbox'][1] and eq_bbox[3] >= block['bbox'][3]:
        print("ok")
        if eq_bbox[0] > block['bbox'][0]:
            eq_bbox[0] = block['bbox'][0]
        if eq_bbox[2] < block['bbox'][2]:
            eq_bbox[2] = block['bbox'][2]
    elif eq_bbox[1] >= block['bbox'][1] and eq_bbox[3] <= block['bbox'][3]:
        eq_bbox[1] = block['bbox'][1]
        eq_bbox[3] = block['bbox'][3]
        if eq_bbox[0] > block['bbox'][0]:
            eq_bbox[0] = block['bbox'][0]
        if eq_bbox[2] < block['bbox'][2]:
            eq_bbox[2] = block['bbox'][2]
    elif eq_bbox[1] >= block['bbox'][1] and eq_bbox[3] > block['bbox'][3] >= eq_bbox[1]:
        eq_bbox[1] = block['bbox'][1]
        if eq_bbox[0] > block['bbox'][0]:
            eq_bbox[0] = block['bbox'][0]
        if eq_bbox[2] < block['bbox'][2]:
            eq_bbox[2] = block['bbox'][2]
    return eq_bbox


def inline(eq_bbox, block):
    aligned = False
    if (block['bbox'][1]+20>=eq_bbox[1]>= block['bbox'][1]-20):
        aligned = True
    elif (block['bbox'][3]+20>=eq_bbox[3]>= block['bbox'][3]-20):
        aligned = True
    if (block['bbox'][1] - 20 >= eq_bbox[1] >= block['bbox'][1] + 20):
        aligned = True
    elif (block['bbox'][3] - 20 >= eq_bbox[3] >= block['bbox'][3] + 20):
        aligned = True
    elif eq_bbox[1] <= block['bbox'][1] and eq_bbox[3] >= block['bbox'][3]:
        aligned = True
    return aligned

# Driver code
word = 'geeks'
print(split(word))
from typing import List
import fitz
from fitz.fitz import Point, Page, Rect
from pprint import pprint
from itertools import groupby
import json
from image import find_image
from difflib import SequenceMatcher

print(SequenceMatcher(None, 'abcd', 'abce').ratio())

# optional
# import pdfkit

# print(fitz.__doc__)
DOC_NAME = pdf_name
#DOC_NAME = "Tkaczyk2015_Article_CERMINEAutomaticExtractionOfSt.pdf"
# DOC_NAME = "Cheng2020_Chapter_MaximumEntropyRegularizationAn.pdf"
# DOC_NAME = "Zhou2020_Chapter_AnImprovedConvolutionalBlockAt.pdf"
# DOC_NAME = "Das-Jawahar2020_Chapter_AdaptingOCRWithLimitedSupervis.pdf"
# DOC_NAME = "Chakraborty2022_Article_ModelingRight-skewedHeavy-tail.pdf"
#DOC_PATH = BASE_PATH + "/" + DOC_NAME
#doc = fitz.open(f"{DOC_PATH}")
doc = fitz.open(f"{path_to_pdf_file}")
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
index = 0
for page2 in doc:
    num_image_for_page = 0
    eq_bbox = [0, 0, 0, 0]
    fig_caption_coords = []
    index += 1
    if index > 30:
        break
    if index > 0:
        images = page2.get_image_info()
        print("images: "+str(images))
        texts = page2.get_text("json")
        texts = json.loads(texts)
        line = False
        print("len(texts['blocks']): " + str(len(texts['blocks'])))
        #page2.draw_rect(Rect([170, 125, 150, 150]), color=color_rect)
        for block in texts['blocks']:
            #page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
            s = ""
            colored = False
            try:
                print(block['lines'][0]['spans'][0]['text'])
                line = True
            except:
                line = False
                print("Error")
            if line is True:
                for i in range(len(block['lines'])):
                    for j in range(len(block['lines'][i]['spans'])):
                        s += " "+block['lines'][i]['spans'][j]['text']
                        print("i: " + str(i) + " j: " + str(j) + " text: " + block['lines'][i]['spans'][j]['text'])
                        if block['lines'][i]['spans'][j]['text'] == "4 Extraction workﬂow implementation":
                            print('oi')
                            # print(string)
                            x = block['lines'][i]['spans'][j]['text'].split()
                            # print(SequenceMatcher(None, string.replace("'", ""),
                            #                      block['lines'][i]['spans'][j]['text']).ratio())
                            # print(split(x[2]))
                print("phrase: "+s)
                if s.__eq__(" 123") and str(block).__eq__(texts['blocks'][len(texts['blocks'])-1]):
                    page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
                    continue

                for string in l5:
                    # if block['type'] == 0 and (SequenceMatcher(None, string.replace("'", ""),
                    #                                          block['lines'][i]['spans'][j][
                    #                                             'text']).ratio() >= 0.8 or string.replace("'",
                    #                                                                                      "")
                    #                       in block['lines'][i]['spans'][j]['text']) and (
                    #  block['lines'][i]['spans'][j]['flags'] == 20 or
                    #  block['lines'][i]['spans'][j]['flags'] == 6):  # all elements
                    print(block['lines'][0]['spans'][0]['flags'])
                    print(block['lines'][0]['spans'][0]['text'])
                    print(block['lines'][len(block['lines']) - 1]['spans'][
                              len(block['lines'][len(block['lines']) - 1]['spans']) - 1]['flags'])
                    print(block['lines'][len(block['lines']) - 1]['spans'][
                              len(block['lines'][len(block['lines']) - 1]['spans']) - 1]['text'])
                    print(SequenceMatcher(None, string.replace("'", ""), s).ratio() >= 0.8 or string.replace("'",
                                                                                                             "")
                          in s)
                    if (s.__contains__("Implementation Details")):
                        print("oi")
                    if block['type'] == 0 and (
                            SequenceMatcher(None, string.replace("'", ""), s).ratio() >= 0.75 or string.replace("'",
                                                                                                               "")
                            in s) and (
                            (block['lines'][0]['spans'][0]['flags'] == 20 and
                             block['lines'][len(block['lines']) - 1]['spans']
                             [len(block['lines'][len(block['lines']) - 1]['spans']) - 1]['flags'] == 20) or
                            block['lines'][0]['spans'][0]['flags'] == 6):  # all elements

                        page2.draw_rect(Rect(block['bbox']), color=color_textline, width=1.5)

                        #page2.draw_rect(Rect(block['bbox']), color=color_textline, width=1.5)
                        colored = True
                        print("flag: " + str(block['lines'][i]['spans'][j]['flags']))
                    else:
                        finded, box = title_inner(string, block)
                        if finded == True:
                            page2.draw_rect(Rect(box), color=color_textline, width=1.5)

                            page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
                            # page2.draw_rect(Rect(block['bbox']), color=color_textline, width=1.5)
                            colored = True

                        '''
                        for line in block['lines']:
                            page2.draw_rect(Rect(line['bbox']), color=color_textline)

                            page2.add_freetext_annot(
                                Rect(line['bbox'][0] + 110, line['bbox'][1], line['bbox'][2] + 110, line['bbox'][3]), "Title",
                                text_color=color_textline)
                            '''
                if colored.__eq__(False):
                    for fig_caption in figures_caption:
                        if block['type'] == 0 and SequenceMatcher(None, s.replace(" ", ""), fig_caption.replace(" ", "")).ratio()>=0.9:
                            page2.draw_rect(Rect(block['bbox']),
                                            color=color_fig_caption, width=1.5)
                            fig_caption_coords.append([block['bbox'][1], block['bbox'][3]])
                            colored = True
                            num_image_for_page += 1
                if colored.__eq__(False):
                    for tab_caption in tables_caption:
                        if block['type'] == 0 and SequenceMatcher(None, s.replace(" ", ""), tab_caption.replace(" ", "")).ratio()>=0.8:
                            page2.draw_rect(Rect(block['bbox']),
                                            color=color_Tab_caption, width=1.5)
                            colored = True
                if colored.__eq__(False):
                    if eq_bbox != [0, 0, 0, 0]:
                        if eq_bbox[3] < block['bbox'][1] or eq_bbox[1] > block['bbox'][3]:
                            page2.draw_rect(Rect([eq_bbox[0], eq_bbox[1], eq_bbox[2], eq_bbox[3]]),
                                            color=color_word, width=1.5)
                            eq_bbox = [0, 0, 0, 0]
                    for eq in l8:
                        if s.__contains__("⎪ ⎪ ⎪ ⎪ ⎩"):
                            print(s.replace("�", ""))
                            print("bella")
                            print(block['bbox'])
                            print(' '.join(filter(lambda x: x in printable, s)))
                            print(s.replace("-", ""))
                            print(eq)
                            print(eq.replace(" ", "").replace("_",""))
                            print(s)
                            print(s.replace(" ", ""))
                            print(eq.replace(" ", "").replace("_", "").__contains__(
                                s.replace(" ", "").replace("�", "")))
                            print(SequenceMatcher(None, eq.replace(" ", "").replace("_", ""),
                                                  s.replace(" ", "")).ratio())
                            #time.sleep(4)
                        if block['type'] == 0 and (
                                SequenceMatcher(None, eq.replace(" ", "").replace("_", "").replace("^",""), s.replace(" ", "")).ratio() >= 0.69
                                or eq.replace(" ", "").replace("_", "").replace("^","").__contains__(s.replace(" ", "").replace("�", "")
                                                                                     )or s.replace(" ", "").__contains__(eq.replace(" ", "").replace("_", "").replace("^","")
                                                                                     )):
                            print("s equation: " + str(s))
                            eq_bbox = utils(eq_bbox, block)
                            colored = True
                            break
                            #if eq_bbox[1] != 0 and eq_bbox[3] != 0:
                            #    print(eq_bbox)
                            #    page2.draw_rect(Rect([block['bbox'][0], eq_bbox[1], block['bbox'][2], eq_bbox[3]]), color=color_word)
                            #page2.draw_rect(Rect(block['bbox']), color=color_word)
                            # page2.draw_rect(Rect(block['lines'][i]['spans'][j]['bbox']), color=color_word)
                        else:

                            k = len(s.replace(" ", "").replace("�", ""))

                            it_eq = 0
                            if k < len(eq.replace(" ", "")):
                                while it_eq + k <= len(eq):
                                    print("eq: " + str(eq.replace(" ", "")[it_eq:it_eq + k]))
                                    print("k: " + str(k))
                                    print("s: " + str(s))
                                    if SequenceMatcher(None, "f(q)=q", s).ratio() >= 0.7 and SequenceMatcher(
                                            None,
                                            " f(q)=q( 1 + λlogq - λ∑_j p_j logp_j) ",
                                            eq).ratio() >= 0.5:
                                        print(eq)
                                        # time.sleep(4)
                                    # time.sleep(3)
                                    if block['type'] == 0 and SequenceMatcher(None,
                                                                              eq.replace(" ", "").replace("_",
                                                                                                          "").replace("^","")[it_eq:it_eq + k],
                                                                              s.replace(" ", "").replace("�",
                                                                                                         "")).ratio() >= 0.6:
                                        eq_bbox = utils(eq_bbox, block)
                                        colored = True
                                        #if eq_bbox[1] != 0 and eq_bbox[3] != 0:
                                        #    print(eq_bbox)
                                        #    page2.draw_rect(
                                        #        Rect([block['bbox'][0], eq_bbox[1], block['bbox'][2], eq_bbox[3]]),
                                        #        color=color_word)
                                        #page2.draw_rect(Rect(block['bbox']), color=color_word)
                                        break

                                    it_eq += 1
                            if colored.__eq__(False) and s.__contains__(eq[len(eq)-4: len(eq)-1]):# contains
                                # equation number list es.: (1), (2) ...
                                it_s = 0
                                k = len(eq.replace(" ", "").replace("_", "".replace("^","")))
                                if k < len(s.replace(" ", "").replace("�", "")):
                                    while it_s + k <= len(s):
                                        if SequenceMatcher(None, s.replace(" ", "").replace("�","")[it_s:it_s + k], "py=-LCE").ratio()>=0.5:
                                            print("oi")
                                        print("s: " + str(s.replace(" ", "").replace("�","")[it_s:it_s + k]))
                                        print("k: " + str(k))
                                        print("eq: " + str(eq))
                                        if block['type'] == 0 and SequenceMatcher(None,
                                                                                  s.replace(" ", "").replace("�","")[it_s:it_s + k],
                                                                                  eq.replace(" ", "").replace("_",
                                                                                                             "").replace("^","")).ratio() >= 0.9:
                                            print(s.replace(" ", "").replace("�","")[it_s:it_s + k])
                                            box2 = [0, 0, 0, 0]
                                            for i in range(len(block['lines'])):
                                                eq_embedded=""
                                                box1 = [0, 0, 0, 0]
                                                for j in range(len(block['lines'][i]['spans'])):
                                                    eq_embedded += block['lines'][i]['spans'][j]['text']
                                                    box1 = utils(box1, block['lines'][i]['spans'][j])
                                                if SequenceMatcher(None, eq_embedded, s.replace(" ", "").replace("�","")[it_s:it_s + k]).ratio() >= 0.7:
                                                        #eq_bbox = utils(eq_bbox, box)
                                                        page2.draw_rect(Rect(box1), color=color_word, width=1.5)
                                                        colored = True
                                                        page2.draw_rect(Rect([block['bbox'][0],block['bbox'][1], block['bbox'][2], box1[1]]), color=color_block, width=1.5)

                                            # if eq_bbox[1] != 0 and eq_bbox[3] != 0:
                                            #    print(eq_bbox)
                                            #    page2.draw_rect(
                                            #        Rect([block['bbox'][0], eq_bbox[1], block['bbox'][2], eq_bbox[3]]),
                                            #        color=color_word)
                                            # page2.draw_rect(Rect(block['bbox']), color=color_word)
                                            break

                                        it_s += 1
                            #if colored.__eq__(False) and eq_bbox!=[0, 0, 0, 0]:
                            #    page2.draw_rect(Rect(eq_bbox).intersect(Rect(block['bbox'])), color=color_Tab_caption, width=1.5)


                    if eq_bbox[1] != 0 and eq_bbox[3] != 0:
                        print("eq_bbox: "+str(eq_bbox))
                        print(s)
                        #page2.draw_rect(Rect([eq_bbox[0], eq_bbox[1], eq_bbox[2], eq_bbox[3]]),
                         #               color=color_word)

                if colored.__eq__(False):
                    indexes = [i for i in range(0, 101)]
                    lst = []
                    for l in indexes:
                        char = " " + str(l) + ". "
                        print("char: " + str(char))
                        if s.__contains__(char):
                            lst.append(s.rfind(char))
                    print("lst: " + str(lst))
                    lst.sort()

                    for ref in references:
                        if SequenceMatcher(None,
                                           "31. Yepes, A.J.: Conﬁdence penalty, annealing Gaussian noise and zoneout for biLSTM-CRF networks for named entity recognition. arXiv preprint",
                                           s).ratio() >= 0.8 and SequenceMatcher(None,
                                                                                 "31. Yepes, A.J.: Conﬁdence penalty, annealing Gaussian noise and zoneout for biLSTM-CRF networks for named entity recognition. arXiv preprint",
                                                                                 ref).ratio() >= 0.8:
                            print("s: " + s)
                            print("ref: " + ref)
                            print(SequenceMatcher(None, ref, s).ratio())
                            time.sleep(5)
                        '''
                        c = "\n"
                        lst = [0]
                        for pos, char in enumerate(ref):
                            if char == c:
                                lst.append(pos)
                        lst.append(len(ref))
                        '''
                        if s.__contains__("Cheng, C., Huang, Q., Bai, X."):
                            print("yes")
                        print(str(lst) + "  " + s)
                        if len(lst) == 1:
                            if block['type'] == 0 and (
                                    SequenceMatcher(None, s.replace(" ", ""),
                                                    ref.replace(" ", "")).ratio() >= 0.6
                                    or s.replace(" ", "").replace("_", "").__contains__(ref.replace(" ", ""))):
                                page2.draw_rect(Rect(block['bbox']), color=color_references, width=1.5)
                                colored = True
                        for iter in range(0, len(lst) - 1):
                            print("references: " + s[lst[iter]: lst[iter + 1]])
                            if block['type'] == 0 and (
                                    SequenceMatcher(None, s[lst[iter]: lst[iter + 1]].replace(" ", ""),
                                                    ref.replace(" ", "")).ratio() >= 0.6
                                    or s.replace(" ", "").replace("_", "").__contains__(ref.replace(" ", ""))):
                                page2.draw_rect(Rect(block['bbox']), color=color_references, width=1.5)
                                colored = True
            if block['type'] == 1:  # images
                page2.draw_rect(Rect(block['bbox']), color=color_images, width=1.5)
                colored = True
                num_image_for_page -= 1
                if not len(fig_caption_coords).__eq__(0):
                    fig_caption_coords.pop()
            if colored.__eq__(False):
                if eq_bbox != [0, 0, 0, 0] and (Rect(eq_bbox).intersect(Rect(block['bbox'])).get_area() != 0) and not s.__contains__(":"):
                    percentual = Rect(eq_bbox).intersect(Rect(block['bbox'])).get_area()/Rect(eq_bbox).get_area()
                    aligned = inline(eq_bbox, block)
                    if percentual >= 0.7 or Rect(eq_bbox).contains(Rect(block['bbox'])) or aligned or s.__contains__("⎩") or s.__contains__("⎠"):
                        print("ss: "+s)
                        print("percentual: "+str(percentual))
                        eq_bbox = utils(eq_bbox, block)
                        colored=True
                    # eq_bbox = utils(eq_bbox, block)
                    elif not((block['bbox'][1]+5) >= eq_bbox[1] >= (block['bbox'][1]-5)):
                        page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
                elif eq_bbox != [0, 0, 0, 0] and not s.__contains__(":"):
                    aligned = inline(eq_bbox, block)
                    print(aligned)
                    if aligned:
                        eq_bbox = utils(eq_bbox, block)
                        colored = True
                else:
                    page2.draw_rect(Rect(block['bbox']), color=color_block, width=1.5)
    page2.draw_rect(Rect([eq_bbox[0], eq_bbox[1], eq_bbox[2], eq_bbox[3]]), color=color_word, width=1.5)
    if num_image_for_page > 0:
        box_image = find_image(BASE_PATH, DOC_NAME, index-1, fig_caption_coords, color_white=color_white, color_images=color_images)
        if len(fig_caption_coords) >= 2:
            if index == 9:
                print(9)

            tmp = box_image
            inc = 10
            for coord in fig_caption_coords:
                if box_image[1] < coord[0] < box_image[3]\
                        and (box_image[1]/coord[0] < 0.95 or coord[0]/box_image[3] < 0.95):
                    page2.draw_rect(Rect([tmp[0], tmp[1], tmp[2], coord[0]-inc]), color=color_images, width=2)
                    tmp = [box_image[0], coord[1]+inc, box_image[2], box_image[3]]
            page2.draw_rect(Rect(tmp), color=color_images, width=2)
        else:
            page2.draw_rect(Rect(box_image), color=color_images, width=2)

    '''
                        for iter in range(0, len(lst) - 1):
                            if block['type'] == 0 and (
                                    SequenceMatcher(None, ref[lst[iter]: lst[iter + 1]].replace(" ", ""),
                                                    s.replace(" ", "")).ratio() >= 0.6
                                    or ref.replace(" ", "").replace("_", "").__contains__(s.replace(" ", ""))):
                                page2.draw_rect(Rect(block['bbox']), color=color_images)
    '''
# doc.save(f'{BASE_PATH}/Cheng2020_Chapter_MaximumEntropyRegularizationAn_2.pdf')
#doc.save(f'{BASE_PATH}/Zhou2020_Chapter_AnImprovedConvolutionalBlockAt_2.pdf')
# doc.save(f'{BASE_PATH}/Das-Jawahar2020_Chapter_AdaptingOCRWithLimitedSupervis_2.pdf')
# doc.save(f'{BASE_PATH}/Chakraborty2022_Article_ModelingRight-skewedHeavy-tail_2.pdf')
doc.save(f'{BASE_PATH}/'+DOC_NAME.replace(".pdf", "")+'_2.pdf')
