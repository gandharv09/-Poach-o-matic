import scraperwiki
from bs4 import BeautifulSoup
import string
import unicodedata
import time
import json
import csv
import random

def getDepartment(response):
    soup = BeautifulSoup(response, "lxml")
    top_prof = soup.find("div", {"class":"top-info-block"})
    department = top_prof.find("div", {"class":"result-title"}).find('br').previousSibling
    return department.strip()

with open('Top_100_University.csv', 'r') as f:
    reader = csv.reader(f)
    univ_list = list(reader)

f = csv.writer(open('ratemyprofessors_data.csv', 'w'))
f.writerow(["averageratingscore_rf", "pk_id", "total_number_of_ratings_i", "teacherfirstname_t'", "teacherlastname_t", "department", "university"])
for i in range(1,len(univ_list)):
    univ = univ_list[i]
    college, sid = univ[-2],univ[-1]
    num = 200
    url = "http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows="+ str(num) +"&callback=noCB&q=*%3A*+AND+schoolid_s%3A"+ sid +"&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf"
    response = scraperwiki.scrape(url)
    response = (response[5:-3])
    response_dict = json.loads(response)
    prof_list = response_dict['response']['docs']
    print(college, len(prof_list))
    for prof in prof_list:
        soup = scraperwiki.scrape("http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(prof["pk_id"]))
        try:
            dep = getDepartment(soup)
            print(prof["teacherfirstname_t"] + prof["teacherlastname_t"])
            f.writerow([prof["averageratingscore_rf"], prof["pk_id"], prof["total_number_of_ratings_i"], prof["teacherfirstname_t"], prof["teacherlastname_t"], dep, college])
        except:
            continue