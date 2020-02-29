# Script for Hounors Project 2020 by Vadims Minciks, 40404598
# generates perceptual hashes for images, calculates hamming distance, and analyses results 
# available in https://github.com/vadimmincik/Hounours-Project-2020
# last update 29/02/2020


from PIL import Image
import imagehash
from imagehash import hex_to_hash
import os
import numpy # to save dictionary
import time # for timing
import random


def hashing(photo_directory, hash_directory): 

    if not os.path.exists(hash_directory):                #directory for storing files with hash values
        os.mkdir(hash_directory)

    algs = {'aHash' : imagehash.average_hash, 'dHash' : imagehash.dhash, 'pHash' : imagehash.phash, 'wHash' : imagehash.whash}
    for alg_name, alg in algs.items():
        
        path = hash_directory + '\\hashes_' + str(alg_name)
        print(f'Hashing {photo_directory[:-1]} with {alg_name}')
        if os.path.exists(path + '.npy'):                           #if file with hashes exists - load it
            hash_dict = numpy.load(path + '.npy',allow_pickle='TRUE').item()
            print(f'  Loading existing dictionary for {str(alg_name)}')
        else:                                                       #else create a clean one
            hash_dict = {'orig' :{}, 'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}}  #dictionary layout
            print(f'  Creating new dictionary for {str(alg_name)}')

        print(f'  Images hashed (out of {len(os.listdir(photo_directory))}):')    #for counter
        counter = 0
        t0 = time.time()
        for image in os.listdir(photo_directory):                         #going through images in directory which was passed as a parameter
            i = alg(Image.open(photo_directory + image))        
            hash_dict[os.path.basename(os.path.normpath(photo_directory))[0:4].lower()][image[:3]] = str(i)   #adding hash value to dictionary 'twit': {234 : <hash value>}
            counter += 1
            if counter % 50 == 0: print(f'  {counter}', end=' ')
        t1 = time.time()
        numpy.save(path, hash_dict)
        print(' ')
        print(f'  Hashing of {photo_directory[:-1]} with {alg_name} finished, total {counter} hashes')
        print(f'  Time taken: {time.strftime("%H:%M:%S", time.gmtime(t1-t0))} \n')
    print(f'  [!] Hashing for this platform done! \n')

def hamming_calc_tp(hash_directory, hamm_directory):

    if not os.path.exists(hamm_directory):        #directory for storing files with hash values
        os.mkdir(hamm_directory)

    for file in os.listdir(hash_directory):       #for every file in directory, which holds hash values
    
        hash_dict = numpy.load(hash_directory+file,allow_pickle='TRUE').item()
        hamm_dict = {'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}}  #dictionary which will hold hamming distances               

        for platform, hashes in hash_dict.items():                  #for each platform (facebook, instagram..)
            if platform == 'orig': continue                         #skip originals, because other platforms are compared to it       
            for image, hash_value in hashes.items():                #image name and hash value inside this platfrom dictionary
                hamming_distance = hex_to_hash(hash_dict['orig'][image]) - hex_to_hash(hash_value)  #origonal file hash minus processed file hash
                #normalising - divided by length of hash (each hex value is 4 bits), and rounded up to 0,xxx so all values are same length
                hamming_distance = round(hamming_distance/(len(hash_value)*4), 3)     
                hamm_dict[platform][image] = hamming_distance       #add hamming distance to corresponding dictionoary ({'face' :{}...)                     

        numpy.save(hamm_directory + '\\hamm_dist_tp_' + file[7:12] , hamm_dict)   #save to separata file for each algorithm
        print(f'Hamming distance for {file[7:12]} saved')
               
    print('Hamming distance for all algotithms calculated and saved - True Positive Test')


def hamming_calc_tn(number_of_runs, hash_directory, hamm_directory):

    if not os.path.exists(hamm_directory):        #directory for storing files with hash values
        os.mkdir(hamm_directory)

    for i in range(number_of_runs):     #each run

        hamm_dict = {'aHash': {'orig' :{}, 'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}},
                     'dHash': {'orig' :{}, 'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}},
                     'pHash': {'orig' :{}, 'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}},
                     'wHash': {'orig' :{}, 'face' :{}, 'twit': {}, 'goog':{}, 'inst':{}}}  #dictionary which will hold hamming distances
        test_hash_dict = numpy.load(hash_directory+os.listdir(hash_directory)[0],allow_pickle='TRUE').item()  # load first dictionary to choose a random test image from
        rand_photo = random.choice(list(test_hash_dict['orig'].keys()))               # get one random photo from originals
        print(f'Random photo chosen: {rand_photo}')

        for file in os.listdir(hash_directory):                                           # for every hashing algorithm, which holds hash values
            hash_alg = file[7:12]                                           # getting algorithm name
            hash_dict = numpy.load(hash_directory+file, allow_pickle='TRUE').item()        # loading dictionaru for this algorithm
            test_hash = hex_to_hash(hash_dict['orig'][rand_photo])          # getting hash of random photo for this algorithm
            for platform, hashes in hash_dict.items():                      # for each platform, incl orig (facebook, instagram..)
                for image, hash_value in hashes.items():                    # for each image name and hash value inside this platfrom dictionary
                    hamming_distance = test_hash - hex_to_hash(hash_value)
                    hamming_distance = round(hamming_distance/(len(hash_value)*4), 3) #normalising and rounding up
                    hamm_dict[hash_alg][platform][image] = hamming_distance # add hamming distance to corresponding dictionoary

        numpy.save(hamm_directory + '\\hamm_dist_tn_' + rand_photo, hamm_dict)   #save to separata file for each run

        print('All hashes calculated and saved for this run')
        


def hamming_analyse_tp(hamm_directory, threshold):
    print('TRUE POSITIVE ANALYSIS \n')         

    total_counter = 0
    for file in os.listdir(hamm_directory):
        #if file[13:18] == 'dHash':         #can specify which algarithm to analyse: aHash, dHash, pHash, wHash
            hamm_dict = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
            print(f'[*] Loading hamming distance values for {file[13:18]}')
            alg_counter = 0
            for platform, values in hamm_dict.items():
                #if platform == 'goog':     #can specify which platform to analyse: goog, inst, face, twit
                    print('[-] platform: ' + platform.replace('face', 'Facebook').replace('inst', 'Instagram')\
                          .replace('goog', 'Google Photos').replace('twit', 'Twitter'))
                    problem_images = []
                    for image, hamm_distance in values.items():
                        if hamm_distance >= threshold:
                            print(f'    Hamming distance for image {image} is high - {hamm_distance}')  #prints a warning if hamming distance is high
                            problem_images.append(image)
                            alg_counter +=1
                            total_counter +=1
                    if len(problem_images) > 0:
                        print(f'[!] {len(problem_images)} images with hashing distance over threshold found')
                        for image in problem_images: print('    ' + image)
            print(f'[!] Total problem images for {file[13:18]}: {alg_counter} \n')
    print(f'Total problem images: {total_counter} \n')


def hamming_count_tp(hamm_directory):
    
    #counting how many matches for each hamming distance
    for file in os.listdir(hamm_directory):
        count = {}
        hamm_dict = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
        print(file[13:18])
        for platform, values in hamm_dict.items():
            print(platform)
            for image, hamm_distance in values.items():
                if  hamm_distance in count:
                    count[hamm_distance] +=1
                else:
                    count[hamm_distance] = 1
            #print(count) unsorted
            for hamm_dist in sorted(count):
                print(f'{hamm_dist}: {count[hamm_dist]}')          
            count = {}



def hamming_analyse_tn(hamm_directory, threshold):
    print('TRUE NEGATIVE ANALYSIS \n')
    print(f'Direcotry contains {len(os.listdir(hamm_directory))} files to analyse. For runs with random images:')
    for file in os.listdir(hamm_directory):
        print(file[13:16])
    print('\n')

    total_counter = 0
    for file in os.listdir(hamm_directory):       
        #if file[13:16] == '516':         #can specify which run to analyse
            hamm_dict = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
            print(f'[*] Loading hamming distance values for random photo {file[13:16]}')
            for alg, all_hashes in hamm_dict.items():
                if alg == 'aHash':         #can specify which algarithm to analyse: aHash, dHash, pHash, wHash
                    print(f'[!] Analysing algorithm: {alg} \n')
                    alg_counter = 0
                    for platform, values in all_hashes.items():
                        #if platform == 'goog':     #can specify which platform to analyse: goog, inst, face, twit
                            print('platform: ' + platform.replace('face', 'Facebook').replace('inst', 'Instagram')\
                                  .replace('goog', 'Google Photos').replace('twit', 'Twitter').replace('orig', 'Originals'))
                            problem_images = []
                            for image, hamm_distance in values.items():
                                if hamm_distance <= threshold and image != file[13:16]:      #exclude known matching image
                                    print(f'   - Hamming distance for image {image} is low - {hamm_distance}')
                                    problem_images.append(image)
                                    alg_counter +=1
                                    total_counter +=1
                            
                            if len(problem_images) > 0:
                                print(f'   {len(problem_images)} images with hashing distance under threshold found:')
                                for image in problem_images:
                                    print('   - ' + image)
                                    
                            
                    print(f'Total problem images for {alg}: {alg_counter} \n')
                    
            print(f'Total problem images for test image {file[13:16]}: {total_counter} \n')
            total_counter = 0
    

def hamming_count_tn(hamm_directory):
    
    #different code from tp to accomodate different storage of data
    for file in os.listdir(hamm_directory): #for each run 
        count = {}
        data = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
        print('for random image: ' + file[13:16])
        for alg, platforms in data.items():
            print (alg)
            for platform, values in platforms.items():
                print(platform)
                for image, hamm_distance in values.items():
                    if  hamm_distance in count:
                        count[hamm_distance] +=1
                    else:
                        count[hamm_distance] = 1
                for hamm_dist in sorted(count):
                   print(f'{hamm_dist}: {count[hamm_dist]}')
                      
                count = {}  

def hamming_count_tn_2(hamm_directory):
    
    #different code from tp to accomodate different storage of data
    #sorts hamming distance by categories instead of counting each one
    for file in os.listdir(hamm_directory): #for each run 
        ctr1 = ctr2 = ctr3 = ctr4 = ctr5 = ctr6 = ctr7 = ctr8 = ctr9 = ctr10 = 0
        data = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
        print('for random image: ' + file[13:16])
        for alg, platforms in data.items():
            print (alg)
            for platform, values in platforms.items():
                print(platform)
                for image, hamm_distance in values.items():
                    if  hamm_distance < 0.1: ctr1 += 1
                    elif hamm_distance < 0.2: ctr2 += 1
                    elif hamm_distance < 0.3: ctr3 += 1
                    elif hamm_distance < 0.4: ctr4 += 1
                    elif hamm_distance < 0.5: ctr5 += 1
                    elif hamm_distance < 0.6: ctr6 += 1
                    elif hamm_distance < 0.7: ctr7 += 1
                    elif hamm_distance < 0.8: ctr8 += 1
                    elif hamm_distance < 0.9: ctr9 += 1                    
                    else: ctr10 += 1

                print (f'0-0.1: {ctr1}')
                print (f'0.1-0.2: {ctr2}')
                print (f'0.2-0.3: {ctr3}')
                print (f'0.3-0.4: {ctr4}')
                print (f'0.4-0.5: {ctr5}')
                print (f'0.5-0.6: {ctr6}')
                print (f'0.6-0.7: {ctr7}')
                print (f'0.7-0.8: {ctr8}')
                print (f'0.8-0.9: {ctr9}')
                print (f'0.9-1: {ctr10}')
                    
                ctr1 = ctr2 = ctr3 = ctr4 = ctr5 = ctr6 = ctr7 = ctr8 = ctr9 = ctr10 = 0


def hamming_count_tn_tot(hamm_directory):

    # counts total of matches for all runs and all platforms, for each algorithm
    
    count_a = {}    # dictionaries to hold results for each algorithm
    count_d = {}
    count_p = {}
    count_w = {}
    for file in os.listdir(hamm_directory): #for each run 
        data = numpy.load(hamm_directory+file,allow_pickle='TRUE').item()
        for alg, platforms in data.items():           
            for platform, values in platforms.items():
                for image, hamm_distance in values.items():
                    if alg == 'aHash':                                         
                        if  hamm_distance in count_a:
                            count_a[hamm_distance] +=1
                        else: 
                            count_a[hamm_distance] = 1
                    elif alg == 'dHash':                                         
                        if  hamm_distance in count_d:
                            count_d[hamm_distance] +=1
                        else:
                            count_d[hamm_distance] = 1
                    elif alg == 'pHash':                                         
                        if  hamm_distance in count_p:
                            count_p[hamm_distance] +=1
                        else:
                            count_p[hamm_distance] = 1
                    elif alg == 'wHash':                                         
                        if  hamm_distance in count_w:
                            count_w[hamm_distance] +=1
                        else:
                            count_w[hamm_distance] = 1
                    else: print("error: " + alg)
    # printing results for each algorithm
    print('aHash')
    for hamm_dist in sorted(count_a):
        print(f'{hamm_dist}: {count_a[hamm_dist]}')
    print('dHash')
    for hamm_dist in sorted(count_d):
        print(f'{hamm_dist}: {count_d[hamm_dist]}')                      
    print('pHash')
    for hamm_dist in sorted(count_p):
        print(f'{hamm_dist}: {count_p[hamm_dist]}')                  
    print('wHash')
    for hamm_dist in sorted(count_w):
        print(f'{hamm_dist}: {count_w[hamm_dist]}')                
          
def main():

        # defining directories
    cur_dir = 'C:\\Users\\Vadim\\Desktop\\Honours project\\Testing\\'
    hash_dir = 'Scripts\\hash_values\\'
    hamm_dir_tp = 'Scripts\\hamming_distance_tp\\'
    hamm_dir_tn = 'Scripts\\hamming_distance_tn\\'
    orig_dir = 'Photos\\Originals\\'
    face_dir = 'Photos\\Facebook\\'
    inst_dir = 'Photos\\Instagram\\'
    twit_dir = 'Photos\\Twitter\\'
    goog_dir = 'Photos\\Google\\'

    os.chdir(cur_dir)

        # sending directories of photos to hash
        # parameters: directory with photos and directory to save hashes 
    hashing(orig_dir, hash_dir)   
    hashing(face_dir, hash_dir)
    hashing(inst_dir, hash_dir)  
    hashing(twit_dir, hash_dir)
    hashing(goog_dir, hash_dir)
        
        # calculating hamming distances for true positive test, from values calculated by hashing()
        # parameters: directory with hashes and where to save results
    hamming_calc_tp(hash_dir, hamm_dir_tp)
    
        # calculating hamming distances for true negative test
        # parameters: how many runs, directory with stored hashes, directory to save results
    hamming_calc_tn(1, hash_dir, hamm_dir_tn) 


        # analysing results from hamming_calc_tp() - true positive
        # parameters: directory with stored hashes for true positive, and threshold on scale 0-1
    hamming_analyse_tp(hamm_dir_tp, 0.1)    
    hamming_count_tp(hamm_dir_tp)      #count instances of each hamming distance for true positive

        # analysing results from hamming_calc_tn() - true negative
        # parameters: directory with stored hashes for true negative, and threshold on scale 0-1    
    hamming_analyse_tn(hamm_dir_tn, 0.001)    
    hamming_count_tn(hamm_dir_tn)       #count instances of each hamming distance for true negative
    hamming_count_tn_2(hamm_dir_tn)     #same as previous, but categorises mathces by 0-0.1, 0.1-0.2 etc.
    hamming_count_tn_tot(hamm_dir_tn)   #same as first, but total for all runs
    



if __name__ == '__main__':
	main()
