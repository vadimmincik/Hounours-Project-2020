# Script for Hounors Project 2020 by Vadims Minciks, 40404598
# renames jpg images in a given directory to consequtive numbers up to 999
# available in https://github.com/vadimmincik/Hounours-Project-2020
# last update 29/02/2020

import os

i = 0

cur_dir = 'C:\\Users\\Vadim\\Desktop\\Honours project\\Testing Data'
direcroty = "Twitter\\"
os.chdir(cur_dir)


for filename in os.listdir(direcroty):
    if i < 10:
        dst ="00" + str(i) + ".jpg"
    elif i < 100:
        dst ="0" + str(i) + ".jpg"
    else: dst = str(i) + ".jpg"
    src = direcroty + filename 
    dst = direcroty + dst
    
    os.rename(src, dst) 
    i += 1
    if i%100 == 0:
        print (f"{i} photos renamed")

    
