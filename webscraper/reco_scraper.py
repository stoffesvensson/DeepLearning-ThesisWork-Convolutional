# -*- coding: utf-8 -*-

"""
Spyder Editor

This is a temporary script file.
"""

import requests
import bs4

class RecoWebScraper(object):
    
    def __init__(self):
        self.listOfRatings = []
        self.companies = ['nytorget-6', 'sveabad', 'inred-se-stockholm', 
                          'furniturebox', 'forma-traningscenter-kallhall', 
                          'kung-carls-bakficka', 'restaurang-rakan-stockholm',
                          'allmanna-rorjouren', 'salong-gloss-stockholm', 
                          'kiropraktorkedjan-matton-jernberg-kungsgatan-stockholm',
                          'forma-traningscenter-hasselby', 'lunds-kakeltjanst-lund-kalkstensvagen-33',
                          'restaurang-bankomat-odenplan', 'timmermans-1857',
                          'allinc-stockholm', 'wallberghalsan', 'stance-juristbyra',
                          'svensk-utemiljo', 'crystone-ab', 'webhallen-sverige-ab',
                          'jajja-media-group-ab', 'fonsterexperterna', 'ica-folkes-livs',
                          'cdon-ab', 'trademax-mobler', 'koncern-hk', 'tele2-ab',
                          'qall-telecom', 'com-hem-ab', 'bahnhof-publ-stockholm', 
                          'akono-ab', 'aktiv-kvinna-sodermalm', 'e-stad-i-norden',
                          'hemfrid', 'orgryte-stad', 'key-code-security-ab']
        self.token = 'organisationen'
        self.amount_pages = 14
        
    def init_scrape_websites(self):
        for company in self.companies:
            self.company_name = company
            for pages in range(7, self.amount_pages):
                print("Extracting data from: {0} on page {1}".format(self.company_name, pages + 1))
                if (pages + 1) == 1:
                    self.request = requests.get("https://www.reco.se/" + self.company_name)
                else:
                    self.request = requests.get("https://www.reco.se/" + self.company_name + "?page=" + str(pages + 1))
                self.soup = bs4.BeautifulSoup(self.request.content, "html.parser")
                self.scrape_website(self.soup, self.company_name)
    
    def scrape_website(self, soup, company):
        list_of_ul = soup.find(id = "review-list")
        if list_of_ul:
            list_of_li = list_of_ul.find_all("li")
            company = company.replace("-", " ")
            
            for row_number in range(0, len(list_of_li)):
                review = { 'text': "", 'rating': "", 'points': 0}
                review_text = list_of_li[row_number].find("div", attrs = {'class': 'ln3'})
                review_points = list_of_li[row_number].find("div", attrs = {'class': 'reco-rating rs'})
                review_points = review_points.find_all("span")
                text = ""
                
                for sentence in review_text:
                    if isinstance(sentence, bs4.element.NavigableString):
                        sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
                        text += sentence_string.lower()
                
                if text.find(company) > -1:
                    text = text.replace(company, self.token)
                    
                review['text'] = text
                if len(review_points) < 3:
                    review['rating'] = 'negative'
                elif len(review_points) > 3:
                    review['rating'] = 'positive'
                else:
                    review['rating'] = 'neutral'      
                review['points'] = len(review_points)
                self.listOfRatings.append(review)
                
    def get_list(self):
        return self.listOfRatings   


"""
    Rating 1-2 (0.0 - 2.4)
        1. 'key-code-security-ab' = 1.1 (48 omdömen),
        2. 'com-hem-ab' = 1.5 (245 omdömen),
        3. 'ica-folkes-livs' = 1.6 (40 omdömen),
        4. 'tele2-ab' = 1.6 (57 omdömen),
        5. 'trademax-mobler' = 1.9 (49 omdömen),
        6. 'koncern-hk' = 2.0 (40 omdömen),
        7. 'bahnhof-publ-stockholm' = 2.0 (45 omdömen),
    
    Rating 3  (2.5 - 3.4)
        1. 'furniturebox'= 2.6 (36 omdömen),
        2. 'qall-telecom' = 2.7 (284 omdömen),
        3. 'sveabad' = 2.9 (87 omdömen),
        4. 'inred-se-stockholm' = 2.9 (103 omdömen),
        5. 'cdon-ab' = 2.9 (64 omdömen),
        6. 'crystone-ab' = 3.3 (138 omdömen),
        7. 'aktiv-kvinna-sodermalm' = 3.4 (40 omdömen),
        
    Rating 4-5 (3.5 - 5.0)
        1. 'allmanna-rorjouren' = 3.5 (296 omdömen),
        2. 'stance-juristbyra' = 3.5 (52 omdömen),
        3. 'webhallen-sverige-ab' = 3.5 (66 omdömen),
        4. 'kung-carls-bakficka' = 3.6 (235 omdömen),
        5. 'forma-traningscenter-kallhall' = 3.7 (100 omdömen),
        6. 'restaurang-bankomat-odenplan' = 3.8 (229 omdömen),
        7. 'lunds-kakeltjanst-lund-kalkstensvagen-33' = 3.9 (80 omdömen),
        8. 'kiropraktorkedjan-matton-jernberg-kungsgatan-stockholm' = 4.0 (88 omdömen),
        9. 'restaurang-rakan-stockholm' = 4.0 (106 omdömen),
        10. 'allinc-stockholm' = 4.0 (163 omdömen),
        11. 'wallberghalsan' = 4.0 (101 omdömen),
        12. 'jajja-media-group-ab' = 4.0 (88 omdömen),
        13. 'akono-ab' = 4.0 (277 omdömen),
        14. 'hemfrid' = 4.0 (1346 omdömen),
        15. 'orgryte-stad' = 4.1 (266 omdömen),
        16. 'forma-traningscenter-hasselby' = 4.1 (196 omdömen),
        17. 'fonsterexperterna' = 4.1 (180 omdömen),
        18. 'e-stad-i-norden' = 4.1 (139 omdömen),
        19. 'salong-gloss-stockholm' = 4.2 (70 omdömen),
        20. 'svensk-utemiljo' = 4.2 (83 omdömen),
        21. 'timmermans-1857' = 4.2 (471 omdömen),
        22. 'nytorget-6' = 4.1 (2882 omdömen),
        

"""

