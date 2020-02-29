# Script for Hounors Project 2020 by Vadims Minciks, 40404598
# available in https://github.com/vadimmincik/Hounours-Project-2020
# script that checks how many images are baselien and how many progressive in given directory
# based on the principle that Image.open(image).info["progressive"] returns 1 if file is progressive
# and exception if this key does not exists - which means that its baseline

from PIL import Image
import os

os.chdir("C:\\Users\\Vadim\\Desktop\\Honours project\\Testing Data")
directory = "Original\\"
counter_baseline = 0
counter_progressive = 0
for image in os.listdir(directory): 
    try:
        x = Image.open(directory + image).info["progressive"]
        counter_progressive +=1
    except KeyError:
        counter_baseline +=1

print(f"in {directory[:-1]} - baseline images: {counter_baseline}, progressive images {counter_progressive}")
