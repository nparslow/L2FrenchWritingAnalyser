#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

__author__ = 'nparslow'


import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

base = "http://projekt.ht.lu.se/fileadmin/user_upload/project/cefle/showXmlFile.html?text=Cecilia&level=1"

page = "http://projekt.ht.lu.se/cefle/textes/le-sous-corpus-longitudinal/cecilia/"

driver = webdriver.Firefox()

driver.get(page)

el = driver.find_element_by_class_name("printable").click()
#driver.click("link="+base)
#driver.find_element_(base).click()

#el = driver.find_element_by_class_name("printable")
#webdriver.ActionChains(driver).move_to_element(el).click(el).perform()

source = driver.page_source
print el
print source

driver.close()