import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)


def get_started():
    """
    Initalizes setup.
    """
    driver.get('https://leme.library.utoronto.ca/lexicons/276/details#fulltext')
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'small')))
    element.clear()
    element.send_keys(9)

def increase_page_number(page_number):
    """
    increase page number
    """
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'small')))
    element.clear()
    element.send_keys(page_number)


def check_if_relevant():
    """
    Abstracting out logic to check xml for 'a' or 'n' tag.
    """
    xml = driver.find_elements(By.CLASS_NAME, 'scrollable-text code')
    print (xml)


def scrape_lexicon():
    """
    Work actually happens here.
    """
    get_started()
    list_of_words = driver.find_elements(By.CLASS_NAME, 'line-entry')
    source_encoding = driver.find_element(By.ID, 'source-encoding')
    for i in list_of_words:
        i.click()
        time.sleep(.08)
        #make sure we have time here to wait for popup
        source_encoding.click()

def iterate_through_items_on_first_page():
    """
    First page is half text and this seems to be breaking my logic. So I'm hard-coding in the values for this one.
    """
    print("Page 9 (remember this one's diff diff)")
    for i in range(13, 24):
        word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
        word.click()
        source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
        source_encoding.click()
        

def iterate_though_items_on_all_other_pages():
    """
    Should work for all other pages
    """
    #first_item = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lex-fulltext"]/div/div[3]/div[2]'))) #issue is here I think
    #first_item.click()
    words = driver.find_elements(By.CLASS_NAME, 'line-entry')
    amount_of_words = len(words)
    for i in range(2, amount_of_words):
        try:
            if driver.find_element(By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a'):
                word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
                text = word.text
                print(text)
                word.click()
                source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
                source_encoding.click()
        except Exception as e:
            print(e)
            continue

        #source_text = source_encoding.text
        #print(source_text)


def practice():
    """
    Testing portions of my functions to debug.
    """
    get_started()
    iterate_through_items_on_first_page()
    for i in range(10, 20):
        print(f"Page {i}")
        increase_page_number(i)
        time.sleep(.5)
        iterate_though_items_on_all_other_pages()
    time.sleep(20)
    #check_if_relevant()

#get_started()
#wait = WebDriverWait(driver, 10)
#wordtext = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lex-fulltext"]/div/div[3]/div[18]/a')))
#wordtext.click()
#source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
#source_encoding.click()
#time.sleep(20)

practice()

""" driver.get('https://leme.library.utoronto.ca/lexicons/276/details#fulltext')
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'small')))
element.clear()
element.send_keys(10)
increase_page_number(10)
time.sleep(1)
words = driver.find_elements(By.CLASS_NAME, 'line-entry')
amount_of_words = len(words)
print (amount_of_words)
for i in words:
    print(i.xpath) """

""" for i in range(2, amount_of_words):
        print(f'{i}')
        if driver.find_element(By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a'):
            word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
            text = word.text
            print(text)
            word.click()
            source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
            source_encoding.click()
        else:
            continue """

"""     for i in range(2, amount_of_words):
        if driver.find_element(By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/xref'):
            continue
        
        word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
        text = word.text
        print(text)
        word.click()
        source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
        source_encoding.click() """