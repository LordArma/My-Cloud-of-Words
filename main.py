# This Python file uses the following encoding: utf-8

import re
import platform

import arabic_reshaper
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bidi.algorithm import get_display
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
from wordcloud import WordCloud


def read_text():
    f = open("input.txt", "r")
    return f.read()


def remove_stops(text):
    f = open("stops.txt", "r")
    lines = f.readlines()
    for line in lines:
        text = text.replace("[", " ")
        text = text.replace("]", " ")
        text = text.replace('"', ' ')
        text = text.replace("^", " ")

        text = re.sub("[۱۲۳۴۵۶۷۸۹۰{}()«»?؟@:.;،؛!'ـ-]", " ", text)

        text = text.replace("‌", " ")
        text = text.replace(f" {line.strip()} ", " ")
        text = text.replace(f"\n{line.strip()} ", " ")
        text = text.replace(f" {line.strip()}\n", " ")
        text = text.replace(f"\\n{line.strip()} ", " ")
        text = text.replace(f" {line.strip()}\\n", " ")
        text = text.replace(f"\\r\\n{line.strip()} ", " ")
        text = text.replace(f" {line.strip()}\\r\\n", " ")
    return text


def make():
    the_text = read_text()
    the_text = remove_stops(the_text)

    osname = platform.system()

    if osname == 'Darwin':
        the_text = arabic_reshaper.reshape(the_text)
        the_text = get_display(the_text)

    font_path = 'Vazir.ttf'

    mask = np.array(Image.open('python.jpg'))
    mask_colors = ImageColorGenerator(mask)

    wc = WordCloud(stopwords=STOPWORDS, font_path=font_path,
                   mask=mask, background_color="white",
                   max_words=400, max_font_size=180,
                   random_state=42, width=5000,
                   height=5000, color_func=mask_colors)

    wc.generate(the_text)
    plt.figure(figsize=(5000 / 72, 5000 / 72), dpi=72)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.savefig('example.jpg', bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    make()
