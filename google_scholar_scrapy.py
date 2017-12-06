from selenium import webdriver
import csv
import time
from bs4 import BeautifulSoup
import random
import sys

with open('Top_100_University.csv', 'r') as f:
    reader = csv.reader(f)
    univ_list = list(reader)

start = int(sys.argv[1])
end = int(sys.argv[2])
file_name = "google_scholar_data_" + str(start) + "_" + str(end) + ".csv" 
f = csv.writer(open(file_name, 'w', encoding='utf-8'))
f.writerow(["name", "university", "rank", "url", "cit", "cit_2012", "hid", "hid_2012", "citations", "papers"])

def getProfile(driver):

	box = driver.find_element_by_xpath('//*[@id="gsc_rsb_cit"]')
	hist = box.find_element_by_class_name('gsc_md_hist_b')
	table = box.find_element_by_id('gsc_rsb_st')
	rows = table.find_elements_by_tag_name('tr')
	cit = rows[1].text.split(" ")
	hid = rows[2].text.split(" ")
	data = [cit[1], cit[2], hid[1], hid[2]]

	driver.find_element_by_xpath('//*[@id="gsc_a_ha"]').click()
	first = 0
	citations = 0
	papers = 0
	flag = False
	while True:
		try:
			table = driver.find_element_by_xpath('//*[@id="gsc_a_b"]')
			rows = table.find_elements_by_tag_name('tr')
			if first >= len(rows):
				data.extend([citations, papers])
				print(data[0], data[1], data[2],data[3], data[4], data[5])
				return data
			for i in range(first, len(rows)):
				row = rows[i]
				cit = ""
				yer = ""
				try:
					cit = cit + row.find_element_by_class_name('gsc_a_c').find_element_by_tag_name('a').text
					yer = row.find_element_by_class_name('gsc_a_y').text
				except:
					continue
				
				if len(cit) == 0:
					cit = 0
				if(int(yer) < 2012):
					flag = True
					break
				citations = citations + int(cit)
				papers = papers + 1
			if flag == True:
				data.extend([citations, papers])
				print(data[0], data[1], data[2],data[3], data[4], data[5])
				return data
			else:
				driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]').click()
				first = len(rows)
				time.sleep(random.randint(1,3))
		except:
				data.extend([citations, papers])
				print(data[0], data[1], data[2],data[3], data[4], data[5])
				return data
	return data

path_to_chromedriver = 'C:/Users/Gandharv/Documents/Fall17/Data Science/Project/selenium/chromedriver_win32/chromedriver' # change path as needed
#PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % PROXY)

for i in range(start, (end+1)):
	univ = univ_list[i]
	college = univ[1]
	print("========= ", college, " ==========")
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	browser  = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
	#browser = webdriver.Chrome(executable_path = path_to_chromedriver) #chrome_options=chrome_options
	url = 'http://scholar.google.com/'
	browser.get(url)
	browser.find_element_by_id('gs_hdr_tsi').send_keys(college)
	browser.find_element_by_xpath('//*[@id="gs_hdr_tsb"]').click()
	time.sleep(random.randint(1,3))
	browser.find_element_by_xpath('//*[@id="gs_hdr_mnu"]').click()
	time.sleep(random.randint(1,3))
	browser.find_element_by_xpath('//*[@id="gs_hdr_drw_in"]/div[2]/div[1]/a[3]').click()
	page = 1
	max_page = 50
	while(page <= max_page):
		prof_list = browser.find_element_by_id('gsc_sa_ccl').find_elements_by_xpath("//*[@class='gsc_1usr gs_scl']")
		for prof in prof_list:
			try:
				prof_name  = prof.find_element_by_class_name("gsc_oai_name").find_element_by_tag_name('a').text
				prof_url = (prof.find_element_by_class_name("gsc_oai_name").find_element_by_tag_name('a')).get_attribute('href')
				prof_name = "minchuan zhou"
				prof_url = "https://scholar.google.com/citations?user=SJ39sJYAAAAJ&hl=en&oi=ao"
				print(prof_name, prof_url)
				options = webdriver.ChromeOptions()
				options.add_argument('--headless')
				options.add_argument('--disable-gpu')
				options.add_argument('--window-size=1200,1100')
				driver  = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
				driver.get(prof_url)
				prof_profile = [prof_name, college, i, prof_url]
				prof_profile.extend(getProfile(driver))
				driver.quit()
				if int(prof_profile[4]) < 1500:
					page = 50
					break
				f.writerow(prof_profile)
				time.sleep(random.randint(1,3))
			except BaseException as e:
				print(e)
				continue	
		page = page + 1	
		browser.find_element_by_xpath('//*[@id="gsc_authors_bottom_pag"]/div/button[2]').click()
		time.sleep(random.randint(1,3))
	browser.quit()