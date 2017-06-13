# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:53:29 2017

@author: Kristoffer
"""

import requests
import bs4
import langdetect

class TrustPilotScraper(object):
    
    def __init__(self):
        self.listOfRatings = []
        self.companies = ['www.vivamondo.se', 'members.com', 'www.rejta.se',
                          'www.blocket.se', 'www.nemid.nu', 'middagsfrid.se',
                          'www.eciggshop.se', 'e-bloss.se', 'www.bahnhof.se',
                          'www.smartphoto.se', 'www.euroflorist.se', 'intima.se', '24.se',
                          'www.mytrendyphone.se', 'www.batterikungen.se', 'www.netonnet.se', 
                          'www.abcleksaker.se', 'www.br-leksaker.se', 'www.barnvagnslagret.se',
                          'www.cdon.se', 'www.cykelkraft.se', 'www.resfeber.se', 'www.travelstart.se',
                          'ctiparty.se', 'klarna.com/sv', 'www.komplett.se', 'www.skruvat.se',
                          'easypark.se', 'bildelaronline24.se', 'vimla.se', 'www.adlibris.com',
                          'www.bythjul.com', 'shop.humle.se', 'trustbuddy.com/se', 'guldbrev.se',
                          'www.sas.se', 'www.skickatarta.se', 'www.ellos.se', 'www.nelly.se',
                          'www.zoovillage.com', 'planboksbutiken.se', 'www.lyko.se', 'swedmart.se',
                          'www.hth.se', 'www.bygghemma.se', 'soffadirekt.se', 'villabutiken.se', 
                          'www.chilli.se', 'www.hemverket.se', 'www.trygghetsexperten.se', 'golvpoolen.se',
                          'drottcompany.se', 'www.plastikplagg.se', '121doc.se', 'www.gents.se',
                          'miacris.com', 'www.sportkost.se', 'www.outdoorexperten.se', 'www.outnorth.se',
                          'seuf.se', 'qliro.com', 'www.staples.se','www.comhem.se', 'www.boxer.se',
                          'www.tretti.se', 'www.coolskins.se', 'lekmer.se', 'www.dtf-travel.se',
                          'www.solfaktor.se', 'www.viagogo.se', 'www.perspektivbredband.se',
                          'www.dhl.se', 'www.sj.se', 'www.homeenter.com', 'zalando.se',
                          'www.modekungen.se', 'tailorstore.se', 'www.beddo.se', 'wegot.se',
                          'lampornu.se', 'www.designdelicatessen.se', 'servicefinder.se',
                          'www.elgiganten.se', 'www.babykul.se', 'www.goboken.se', 'scstyling.com',
                          'motorsweden.se', 'vikoperdinbil.se', 'www.ups.se', 'www.momondo.se',
                          'www.apartdirect.com', 'shirtstore.se', 'delightfulhair.com',
                          'www.noos.se', 'www.el24online.se', 'www.it-shoppen-butik.se',
                          'www.mediamarkt.se', 'www.siba.se', 'www.halebop.se', 
                          'globalcar.se']
        self.token = 'organisationen'
        self.amount_pages = 14
        
    def init_scrape_websites(self):
        for company in self.companies:
            self.company_name = company
            for pages in range(7, self.amount_pages):
                print("Extracting data from: {1} on page {0}".format(pages + 1, self.company_name))
                if (pages + 1) == 1:
                    self.request = requests.get("https://se.trustpilot.com/review/" + self.company_name)
                else:
                    self.request = requests.get("https://se.trustpilot.com/review/" + self.company_name + "?page=" + str(pages + 1))
                self.soup = bs4.BeautifulSoup(self.request.content, "html.parser")
                self.scrape_website(self.soup, self.company_name)
    
    def scrape_website(self, soup, company):
        list_of_review_containers = soup.find(id = "reviews-container")
        if list_of_review_containers:
            list_of_reviews = list_of_review_containers.find_all("div", attrs = {'class': 'review-stack'})
            company = company.replace("-", " ")
            
            for row_number in range(0, len(list_of_reviews)):
                review = { 'text': "", 'rating': "", 'points': 0}
                review_text = list_of_reviews[row_number].find("div", attrs = {'class': 'review-body'})
                review_points = list_of_reviews[row_number].find("div", attrs = {'class': 'star-rating'})
                text = ""
                
                if review_text:
                    for sentence in review_text: 
                        if isinstance(sentence, bs4.element.NavigableString):
                            try:
                                if langdetect.detect(sentence.string) == 'sv':
                                    sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
                                    text += sentence_string.lower()
                            except langdetect.lang_detect_exception.LangDetectException as e:
                                print(e)
                
                if text.find(company) > -1:
                    text = text.replace(company, self.token)
                
                if text != "":
                    review['text'] = text
                    """review['rating'] = int(review_points.attrs['class'][1][-1])"""
                    if int(review_points.attrs['class'][1][-1]) < 3:
                        review['rating'] = 'negative'
                    elif int(review_points.attrs['class'][1][-1]) > 3:
                        review['rating'] = 'positive'
                    else:
                        review['rating'] = 'neutral'
                    review['points'] = int(review_points.attrs['class'][1][-1])
                    self.listOfRatings.append(review)
                
    def get_list(self):
        return self.listOfRatings
    
    
    
    
    
""" 
  Rating 1-2 stars (Trustscore 0.0 - 4.9)
      1. 'www.nemid.nu' = 0.7 (224 omdömen), 
      2. 'www.comhem.se' = 0.9 (199 omdömen),
      3. 'www.boxer.se' = 1.1 (95 omdömen),
      4. 'www.blocket.se' = 1.1 (101 omdömen), 
      5. 'www.mediamarkt.se' = 1.1 (143 omdömen),
      6. 'www.dhl.se' = 1.3 (260 omdömen),
      7. 'www.vivamondo.se' = 1.4 (92 omdömen), 
      8. 'www.homeenter.com' = 1.7 (479 omdömen),
      9. 'www.babykul.se' = 1.8 (75 omdömen),
      10. 'www.siba.se' = 1.9 (63 omdömen),
      11. 'www.cdon.se' = 2.0 (357 omdömen), 
      12. 'www.ellos.se' = 2.5 (95 omdömen),
      13. 'www.rejta.se' = 2.6 (65 omdömen),
      14. 'www.elgiganten.se' = 2.6 (222 omdömen),
      15. 'www.sj.se' = 2.6 (68 omdömen),
      16. 'www.dtf-travel.se' = 2.8 (142 omdömen),
      17. 'www.barnvagnslagret.se' = 2.9 (90 omdömen),
      18. 'www.perspektivbredband.se' = 2.9 (124 omdömen),
      19. 'www.tretti.se' = 2.9 (189 omdömen),
      20. 'globalcar.se' = 2.9 (66 omdömen),
      21. 'qliro.com' = 3.2 (103 omdömen),
      22. 'www.nelly.se' = 3.1 (162 omdömen),
      23. 'www.netonnet.se' = 3.2 (179 omdömen),
      24. 'www.halebop.se' = 3.3 (87 omdömen),
      25. 'www.adlibris.com' = 3.8 (120 omdömen),
      26. 'zalando.se' = 4.1 (125 omdömen),
      27. 'members.com' = 4.1 (292 omdömen), 
      28. 'www.beddo.se' = 4.4 (215 omdömen),
      29. 'www.bahnhof.se' = 4.4 (215 omdömen),
      30. 'www.sas.se' = 4.5 (69 omdömen),
      31. 'bildelaronline24.se' = 4.6 (94 omdömen),
      32. 'www.eciggshop.se' = 4.7 (87 omdömen), 
      33. 'www.viagogo.se' = 4.7 (184 omdömen),
      
      
  Rating 3 stars (Trustscore 5.0 - 6.9)
      1. 'www.zoovillage.com = 5.1 (83 omdömen)',
      2. 'www.ups.se' = 5.1 (312 omdömen),
      3. 'tailorstore.se' = 5.3 (260 omdömen),
      4. 'www.modekungen.se' = 5.3 (195 omdömen),
      5. 'www.it-shoppen-butik.se' = 5.5 (96 omdömen), 
      6. 'swedmart.se' = 5.6 (1514 omdömen),
      7. 'www.outdoorexperten.se' = 5.7 (72 omdömen),
      8. 'trustbuddy.com/se' = 5.7 (90 omdömen),
      9. 'vikoperdinbil.se' = 5.7 (61 omdömen),
      10. 'middagsfrid.se' = 5.8 (372 omdömen),
      11. 'www.apartdirect.com' = 5.8 (65 omdömen),
      12. 'www.outnorth.se' = 5.9 (94 omdömen),
      13. 'www.komplett.se' = 6.0 (79 omdömen),
      14. 'www.coolskins.se' = 6.5 (85 omdömen),
      15. 'seuf.se' = 6.5 (63 omdömen),
      16. 'www.plastikplagg.se' = 6.5 (96 omdömen),
      17. 'www.momondo.se' = 6.5 (106 omdömen),
      18. 'lampornu.se' = 6.6 (332 omdömen),
      19. 'wegot.se' = 6.6 (225 omdömen),
      20. '121doc.se' = 6.7 (150 omdömen),
      21. 'www.solfaktor.se' = 6.7 (250 omdömen),
      22. 'www.travelstart.se' = 6.7 (4048 omdömen),
      23. 'scstyling.com' = 6.7 (275 omdömen),
      24. 'www.noos.se' = 6.7 (247 omdömen),
      25. 'www.bygghemma.se' = 6.8 (768 omdömen),
      26. 'www.hth.se' = 6.8 (113 omdömen),
      27. 'motorsweden.se' = 6.8 (186 omdömen),
      28. 'delightfulhair.com' = 6.8 (1131 omdömen),
      29. 'www.el24online.se' = 6.8 (67 omdömen),
      30. 'klarna.com/sv' = 6.9 (5288 omdömen), 
      31. 'shirtstore.se' = 6.9 (171 omdömen),
      
      
  Rating 4-5 stars (Trustscore 7.0 - 10)
      1. 'www.designdelicatessen.se' = 7.0 (109 omdömen),
      2. 'www.staples.se' = 7.2 (201 omdömen),
      3. 'drottcompany.se' = 7.2 (69 omdömen),
      4. 'planboksbutiken.se' = 7.3 (344 omdömen),
      5. 'e-bloss.se' = 7.4 (216 omdömen), 
      6. 'guldbrev.se' = 7.4 (2420 omdömen),
      7. 'lekmer.se' = 7.5 (13 708 omdömen),
      8. 'villabutiken.se' = 7.5 (149 omdömen),
      9. 'easypark.se' = 7.6 (918 omdömen),
      10. 'www.euroflorist.se' = 7.7 (31 140 omdömen),
      11. 'www.gents.se' = 7.8 (192 omdömen),
      12. 'www.resfeber.se' = 7.8 (93 omdömen), 
      13. 'www.skruvat.se' = 7.9 (18769 omdömen),
      14. 'www.goboken.se' = 7.9 (274 omdömen),
      15. 'soffadirekt.se' = 7.9 (1606 omdömen),
      16. 'miacris.com' = 8.0 (98 omdömen),
      17. 'www.cykelkraft.se' = 8.1 (2054 omdömen), 
      18. 'servicefinder.se' = 8.1 (594 omdömen),
      19. 'www.bythjul.com' = 8.2 (804 omdömen),
      20. 'vimla.se' = 8.3 (167 omdömen),
      21. 'www.skickatarta.se = 8.3 (663 omdömen)',
      22. 'www.lyko.se' = 8.3 (11770 omdömen),
      23. 'www.chilli.se' = 8.3 (5943 omdömen),
      24. 'www.smartphoto.se' = 8.3 (4942 omdömen), 
      25. 'www.sportkost.se' = 8.4 (303 omdömen),
      26. 'www.hemverket.se' = 8.4 (160 omdömen),
      27. 'www.batterikungen.se' = 8.4 (4579 omdömen), 
      28. 'www.mytrendyphone.se' = 8.5 (7854 omdömen), 
      29. 'ctiparty.se' = 8.6 (163 omdömen), 
      30. 'www.br-leksaker.se' = 8.7 (4026 omdömen), 
      31. '24.se' = 8.7 (2696 omdömen),
      32. 'golvpoolen.se' = 8.8 (759 omdömen),
      33. 'intima.se' = 9.1 (299 omdömen), 
      34. 'shop.humle.se' = 9.3 (5675 omdömen), 
      35. 'www.abcleksaker.se' = 9.7 (2260 omdömen), 
      36. 'www.trygghetsexperten.se' = 9.7 (1025 omdömen),
"""