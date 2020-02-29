# Script for Hounors Project 2020 by Vadims Minciks, 40404598
# available in https://github.com/vadimmincik/Hounours-Project-2020
# matches photos from original directory to processed directory and renames them accordingly
# can used readily available files with hashes or create new ones

from PIL import Image
import imagehash
from imagehash import hex_to_hash
import os
import numpy # to save dictionary

###establishing directories###
cur_dir = 'C:\\Users\\Vadim\\Desktop\\Honours project\\Testing Data\\Scripts'
orig_photos_dir = '..\\Original\\'
inst_photos_dir = '..\\testing_inst\\'

os.chdir(cur_dir)

if not os.path.exists("hashorigdict_d.npy"):      #creating file with hashes - only once
    hashorigdict = {}                           #dictionary to store image name and hash value
    print('hashing originals')
    counter = 0
    for x in os.listdir('Original'):
        i = imagehash.phash(Image.open(orig_photos_dir + x))
        hashorigdict[x] = str(i)            #adding hash valuer to dictionary
        counter += 1
        if counter % 25 == 0:
            print(f"hashed {counter} images")
    numpy.save('hashorigdict_d.npy', hashorigdict) 
else: print('hashorigdict_d.npy already exists')


if not os.path.exists("hashinstdict_d.npy"):         #creating file with hashes of processed files 
    hashinstdict = {}
    counter = 0
    print('hashing inst')
    for x in os.listdir(inst_photos_dir):
        i = imagehash.phash(Image.open(inst_photos_dir + x))
        hashinstdict[x] = str(i)
        counter += 1
        if counter % 25 == 0:
            print(f"hashed {counter} images")

    numpy.save('hashinstdict_d.npy', hashinstdict) 

else: print('hashinstdict_d.npy already exists')

# loading files with hashes
hashorigdict = numpy.load('hashorigdict_d.npy',allow_pickle='TRUE').item()
hashinstdict = numpy.load('hashinstdict_d.npy',allow_pickle='TRUE').item()

counter_match = 0
total_match = 0
for orig_value in hashorigdict:
    for inst_value in hashinstdict:     
        i = hex_to_hash(hashorigdict[orig_value]) - hex_to_hash(hashinstdict[inst_value])  # converts to imagehash format          
        if i < 10:      #if hamming distance under 10
            print(f"original photo {orig_value} is matching with Instagram photo {inst_value} with hamming distance {i}")
            counter_match +=1
            if counter_match > 1:
                print (f"!!!!!!Original photo {orig_value} found more than one match")                
            
            #code for renaming and moving to new directory
            src = inst_photos_dir + inst_value
            dst = inst_photos_dir + orig_value
            os.rename(src, dst)
            total_match +=1

    counter_match = 0

print (f"matching done. {total_match} photos out of {len(hashinstdict)} renamed.")



            

               
