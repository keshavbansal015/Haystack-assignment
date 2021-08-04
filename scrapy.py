#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 18:58:45 2021

@author: keshav
"""
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# path for chromedriver
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = uc.Chrome(executable_path='/home/keshav/chromedriver',
				options=options)

# enter keyword to search (URL)
keyword = "https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365"
driver.get(keyword)

# Sorting order:
sorting_order = 'submission-desc'
output_file = 'output.csv'

# create action chain object
action = ActionChains(driver)
try:
	# move to another URL
	element = driver.find_element_by_link_text("See all reviews")

	# perform the operation
	action.click(on_element = element)
	action.perform()
	print("level 1 done! moving onto level 2.\n")

	try:
		# dropdown option select ( most relevant -> newest to oldest )
		element = driver.find_element(By.CSS_SELECTOR, '.field-input')		
		select = Select(element)
		select.select_by_value(sorting_order)
		time.sleep(3)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# Now Scrape
		count_pages=0
		flag = True
		columns=[
				'date',
				'purchase_verified',
				'rating',
				'title',
				'review_text',
				'author'
			]
		df = pd.DataFrame(columns=columns)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		while(flag):
			element_date_texts = []
			element_verifieds = []
			element_ratings = []
			element_titles = []
			element_body_texts = []
			element_authors = []
			# element_likess = []
			# element_dislikess = []

			elements = driver.find_elements(By.CSS_SELECTOR, "div.ReviewList-content")
			print('Pages scraped: ',count_pages)

			for element in elements:

				element_head = element.find_element_by_class_name('review-header')  # stars and title
				element_date = element.find_element_by_class_name('review-date')    # date
				element_body = element.find_element_by_class_name('review-body')	# body
				element_author = element.find_element_by_class_name('review-footer')# author

				# Now start to scrape
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# Review date
				element_date_text = element_date.find_element_by_css_selector('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)').text

				if (element_date_text[-4:] == '2020' and element_date_text[:3] == 'Dec'):
					flag = False
					break
				
				##### For purchase verified #####
				try:
					element_verified = element_date.find_element_by_css_selector('div:nth-child(2)').text
				except:
					element_verified = 'No'
				#####
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# Review rating
				element_rating	= element_head.find_element_by_css_selector('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(3) > span:nth-child(2)') \
									.text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# Review title
				try:
					element_title 	= element_head.find_element_by_css_selector('div:nth-child(1) > h3:nth-child(2)').text
				except:
					element_title 	= ''
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# Review body

				# Review body text
				element_body_text = element_body.find_element_by_tag_name('p').text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
				# Review body likes
				# try:
				# 	likes_element = element_body.find_element(By.CLASS_NAME,'[aria-label="Likes"]') \
				# 						.find_elements(By.TAG_NAME,'li')
				# 	element_likes = []
				# 	for each in likes_element:
				# 		element_likes.append(each.text)
				# except:
				# 	print("Likes not mentioned")
				# 	element_likes = []
				# finally:
				# 	element_likes = element_likes.join(',')
				
				# # Review body dislikes
				# try:
				# 	dislikes_element = element_body.find_element(By.CLASS_NAME'[aria-label="Dislikes"]') \
				# 						.find_elements(By.TAG_NAME,'li')
				# 	element_dislikes = []
				# 	for each in dislikes_element:
				# 		element_dislikes.append(each.text)
				# except:
				# 	print("Dislikes not mentioned")
				# 	element_dislikes = []
				# finally:
				# 	element_dislikes = element_dislikes.join(',')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# Review author
				element_author = element_author.find_element_by_css_selector('div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
				# print(element_date_text,element_verified,element_rating,element_title,element_body_text,element_author)

				element_date_texts.append(element_date_text)
				element_verifieds.append(element_verified)
				element_ratings.append(element_rating)
				element_titles.append(element_title)
				element_body_texts.append(element_body_text)
				element_authors.append(element_author)
				# element_likess.append(element_likes)
				# element_dislikess.append(element_dislikes)
			
			page_data = {
			"date":element_date_texts,
			"purchase_verified":element_verifieds,
			"rating":element_ratings,
			"title":element_titles,
			"review_text":element_body_texts,
			"author":element_authors
			}

			# print(page_data)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			df2 = pd.DataFrame(page_data)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# appending the dataframe
			df = df.append(df2, ignore_index=True)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
			# next page of reviews

			if not (flag):
				break
			if (count_pages!=0):
				next_page = driver.find_elements(By.CSS_SELECTOR,'button.paginator-btn:nth-child(3)')[-1]
			else:
				next_page = driver.find_elements(By.CSS_SELECTOR,'.paginator-btn')[-1]

			count_pages += 1
			action.click(on_element = next_page)
			action.perform()
			time.sleep(1)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
		df.to_csv(output_file, index=False)
		print("Scraping done!!! Hire me please! :-D")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	except Exception as e:
		print('Exception 1: ',e)

except Exception as e:
	print('Exception 2: ',e)

time.sleep(5) # scraping done! 
driver.quit()