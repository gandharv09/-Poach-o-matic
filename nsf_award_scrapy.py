from selenium import webdriver
import csv
import time
import random
import sys

with open('google_scholar_data_1_100.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    prof_list = list(reader)


start = int(sys.argv[1])
end = int(sys.argv[2])

file_name = "nsf_award_data_" + str(start) + "_" + str(end) + ".csv" 
f = csv.writer(open(file_name, 'w', encoding='utf-8'))
f.writerow(["no.", "name", "university", "amount", "num_awards"])

path_to_chromedriver = 'C:/Users/Gandharv/Documents/Fall17/Data Science/Project/selenium/chromedriver_win32/chromedriver' # change path as needed
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1200,1100')				
browser  = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
for i in range(start, end+1):
	name, univ = prof_list[i][0], prof_list[i][1]
	print(name, univ)
	try:
		url = 'https://www.nsf.gov/awardsearch/'
		browser.get(url)
		time.sleep(random.randint(1,3))
		browser.find_element_by_xpath('//*[@id="Field1"]').send_keys(name)
		browser.find_element_by_xpath('//*[@id="simpleSearch"]/a').click()
		time.sleep(random.randint(3,5))
		browser.find_element_by_xpath('//*[@id="simpleSearchPara"]/a').click()
		time.sleep(random.randint(1,3))
		result = browser.find_element_by_id('mainViewId').find_element_by_id('viewId')
		table = result.find_element_by_class_name('x-table-layout-cell')
		rows = table.find_elements_by_class_name('listview-item')

		amount = 0
		num_awd = 0
		for row in rows:
			data = row.text.split(";")
			rel = data[-2].replace('Relevance:', '')
			if(float(rel) > 50):
				award = data[-3]
				award = award.replace(' Award Amount:$', '')
				award = award.replace(',', '')
				amount = amount + float(award)
				num_awd = num_awd + 1
			else:
				break
		print(i, name, univ, amount, num_awd)
		f.writerow([i, name, univ, amount, num_awd])
		time.sleep(random.randint(1,3))
	except:
		f.writerow([i, name, univ, 0, 0])
		browser.quit()
		browser  = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)
		time.sleep(random.randint(1,3))
		continue