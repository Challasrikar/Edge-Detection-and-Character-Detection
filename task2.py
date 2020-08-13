"""
Character Detection

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os

import utils
from task1 import *   # you could modify this line


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/c.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template):
    
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    # TODO: implement this function.
    
    height = len(img)
    width = len(img[0])
    temp_height= len(template)
    temp_width= len(template[0])
    print(height)
    print(width)
    print(temp_height)
    print(temp_width)
    
    NCC = np.zeros((height-temp_height, width-temp_width))
    coordinates=[]
    for y in range(0, height-temp_height):
        for x in range(0, width-temp_width):
            roi = utils.crop(img,y, y+temp_height, x, x+temp_width)
            NCC[y, x] = Normalised_Cross_Correlation(np.asarray(roi), np.asarray(template))
            # The threshold is set to 0.9
            if NCC[y, x] > 0.9:
                print(NCC[y,x])
                coordinates.append((x,y))

    #raise NotImplementedError
    return coordinates

def Normalised_Cross_Correlation(roi, template):
    
    roi_mean=np.mean(roi)
    roi_sub_mean=roi-roi_mean
    temp_mean=np.mean(template)
    temp_sub_mean=template - temp_mean
    numerator = np.sum(np.multiply(roi_sub_mean,temp_sub_mean))
    roi_sub_mean_2=np.multiply(roi_sub_mean,roi_sub_mean)
    temp_sub_mean_2=np.multiply(temp_sub_mean,temp_sub_mean)
    denominator = np.sqrt(np.sum(roi_sub_mean_2)*np.sum(temp_sub_mean_2))
    if(denominator==0):
        ncc = 0
    else:
        ncc = numerator/denominator
    return ncc

def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()
    img = read_image(args.img_path)
    template = read_image(args.template_path)

    coordinates = detect(img, template)

    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)


if __name__ == "__main__":
    main()
