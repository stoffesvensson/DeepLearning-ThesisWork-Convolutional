# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:44:48 2017

@author: Stoffe
"""
import csv
import random
from reco_scraper import RecoWebScraper
from trustpilot_scraper import TrustPilotScraper

""" Instantiate scraper and retrive reviews """
reco = RecoWebScraper()
reco.init_scrape_websites()
list_one = reco.get_list()

""" Instantiate scraper and retrive reviews """
trustpilot = TrustPilotScraper()
trustpilot.init_scrape_websites()
list_two = trustpilot.get_list()

complete_list = list_one + list_two
posArr = []
neuArr = []
negArr = []

pos = 0
neu = 0
neg = 0

""" Split the complete list into three list for the three classes """
for num in range(0, len(complete_list)):
    if complete_list[num]['points'] < 3:
        negArr.append(complete_list[num])
        neg += 1
    elif complete_list[num]['points'] > 3:
        posArr.append(complete_list[num])
        pos += 1
    else:
        neuArr.append(complete_list[num])
        neu += 1

""" 

    The functionality to create the arrays for the training sets 
    
"""        

""" Shuffled list for the first dataset """    
shuffled_list = list(complete_list)
random.shuffle(shuffled_list)

""" Shuffled list for the dataset with the same amount of positive and negative """
halv_posArr = []
halv_posArr_shuffled = list(posArr)
random.shuffle(halv_posArr_shuffled)
for x in range(0, int(len(halv_posArr_shuffled) / 2)):
    halv_posArr.append(halv_posArr_shuffled[x])
shuffled_list_same_amount = halv_posArr + negArr + neuArr
random.shuffle(shuffled_list_same_amount)

""" Shuffled list without neutral reviews """
shuffled_list_without_neu = posArr + negArr
random.shuffle(shuffled_list_without_neu)        
        

""" 

    The functionality to create the arrays for the training sets 
    
"""        

""" instantiate constants """
lengthOne = 449
lengthTwo = 1007
lengthThree = 2007

""" Shuffle neuArr and split the array in two new"""
neuArr2 = []        
random.shuffle(neuArr)
for num in range(0, lengthOne):
    neuArr2.append(neuArr.pop(num))
        
""" Shuffle negArr and split the array in two new"""
negArr2 = []
negArr3 = []
random.shuffle(negArr)
for num in range(0, lengthOne):
    negArr2.append(negArr.pop(num))
for num in range(0, lengthOne):
    negArr3.append(negArr.pop(num))

""" Shuffle posArr and split the array in two """
posArr2 = []
posArr3 = []
random.shuffle(posArr)
for num in range(0, lengthOne):
    posArr2.append(posArr.pop(num))
for num in range(0, lengthOne):
    posArr3.append(posArr.pop(num))

""" Create 2 new lists with the new pos/neg/neu arrays """
list_dataset_test_one = neuArr + negArr2 + posArr2
list_dataset_test_two = neuArr2 + negArr3 + posArr3   
random.shuffle(list_dataset_test_one)    
random.shuffle(list_dataset_test_two)

""" Create 2 new arrays from the review left in negArr """
negArr4 = []
for num in range(0, lengthTwo):
    negArr4.append(negArr.pop(num))

""" Create 2 new arrays from the review left in posArr """    
posArr4 = []
posArr5 = []
for num in range(0, lengthTwo):
    posArr4.append(posArr.pop(num))
for num in range(0, 2007):
    posArr5.append(posArr.pop(num))
    
""" Create 2 new lists with the new pos/neg/ arrays """
list_dataset_test_one_2classes = negArr4 + posArr4
list_dataset_test_two_2classes = negArr + posArr5    
random.shuffle(list_dataset_test_one_2classes)     
random.shuffle(list_dataset_test_two_2classes)

""" Write to csv file. Must change file name and list to the right one before writing """
f = open('testDatasetWithOutNeuTwo', 'w', encoding='utf-8')
try:
    writer = csv.writer(f)
    writer.writerow(('text', 'rating'))
    
    for i in range(0, len(list_dataset_test_two_2classes)):
        writer.writerow((list_dataset_test_two_2classes[i]['text'], list_dataset_test_two_2classes[i]['rating']))
finally:
    f.close()
    
print(open('datasetFullList', 'r', encoding='utf-8').read())