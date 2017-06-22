# Deeplearning - Convolutional Neural network to analyse sentiment in Swedish reviews
This is my thesis work at Linnéuniversity in Kalmar. The research problem was to investigate if deeplearning and a convolutional neural network could be used to analyse sentiment in Swedish reviews. The result was very good on just 2 categories (positive and negative) with 95% accuracy but only 80% accuracy as best on 3 categories (positive, negative and neutral).

Link to thesis: [Sentiment Analysis With Convolutional Neural Networks: Classifying sentiment in Swedish reviews](http://lnu.diva-portal.org/smash/record.jsf?dswid=-8229&pid=diva2%3A1105494&c=8&searchType=SIMPLE&language=en&query=sentiment+analysis&af=%5B%5D&aq=%5B%5B%5D%5D&aq2=%5B%5B%5D%5D&aqe=%5B%5D&noOfRows=50&sortOrder=author_sort_asc&onlyFullText=false&sf=all#sthash.76XXTX1O.dpbs)

## Webscrapers

The two webscrapers scrapes Swedish reviews from www.reco.se and se.trustpilor.com to create 
training datasets for the neural networks. You can either scrape for 3 categories (positive, negative and neutral)
or just for 2 categories (positive and negative).

## CNN-model

In the CNN-model folder is the thesis works research problem. There is a playground file for testing TFlearn and its functionality and a working class to import and use for training a convolutional neural network and to predict swedish reviews.
There are also some existing CNN-models in the folder that could be loaded and used.
