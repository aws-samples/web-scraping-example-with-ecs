# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import boto3
import os
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

def getURL(URL, KEYWORD, ELEMENT_NAME):
    CHROME_PATH = '/usr/local/bin/chromedriver'

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=option, executable_path=CHROME_PATH)        
    driver.get(URL)
    elem = driver.find_element_by_name(ELEMENT_NAME)
    elem.clear()
    elem.send_keys(KEYWORD)
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    time.sleep(3)
    current_url = driver.current_url
    driver.close()
    
    return current_url

def demo():
    URL = "https://www.python.org"
    KEYWORD = "I love python"
    ELEMENT_NAME = "q"  
    current_url = getURL(URL, KEYWORD, ELEMENT_NAME) #Using Selenium to navigate in the web page
    r = requests.get(current_url) #Getting the page using Requests

    soup = BeautifulSoup(r.text, 'html.parser')

    content = [] #Extracting content using BeautifulSoup
    content.append('Extracting all text from a page:\n')
    content.append(soup.get_text())
    content.append('\n\nExtracting all the URLs from a page:\n')

    for link in soup.find_all('a'):
        content.append(link.get('href'))

    str1 = '\n'.join(content)
    
    client = boto3.client('s3') #Saving output to S3 Bucket
    client.put_object(Body=str1, Bucket=os.environ['BUCKET'], Key=os.environ['DESTPATH'] + '/' + str(datetime.now()) + '.txt')


if __name__ == '__main__':
    demo()