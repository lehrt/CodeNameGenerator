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
adjectives = []
nouns = []


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
    source_text_element = driver.find_element(By.XPATH, '//*[@id="mainEntry"]/div/div[1]')
    source_text = source_text_element.text
    type = source_text.split("<")[2]
    specific_word = type.split('"')[1]
    specific_word = specific_word[:-3]
    if "(n)" in type:
        print (f"{specific_word} is a noun")
        nouns.append(specific_word)
    elif "(a)" in type:
        print (f"{specific_word} is an adjective")
        adjectives.append(specific_word)

def find_source_encoding():
    source_encoding = wait.until(EC.element_to_be_clickable((By.ID, 'source-encoding')))
    source_encoding.click()

def scrape_lexicon():
    """
    Work actually happens here.
    """
    get_started()
    iterate_through_items_on_first_page()
    for i in range(10, 15):
        print(f"Page {i}")
        increase_page_number(i)
        time.sleep(.5)
        iterate_though_items_on_all_other_pages()
    print(nouns)
    print(adjectives)
    time.sleep(20)


def iterate_through_items_on_first_page():
    """
    First page is half text and this seems to be breaking my logic. So I'm hard-coding in the values for this one.
    """
    first_word = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lex-fulltext"]/div/div[3]/div[13]/a')))
    first_word.click()
    find_source_encoding()
    for i in range(14, 24):
        word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
        word.click()
        check_if_relevant()
        
def iterate_though_items_on_all_other_pages():
    """
    Should work for all other pages
    """
    words = driver.find_elements(By.CLASS_NAME, 'line-entry')
    amount_of_words = len(words)
    for i in range(3, amount_of_words):
        try:
            if driver.find_element(By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a'):
                word = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="lex-fulltext"]/div/div[3]/div[{i}]/a')))
                text = word.text
                word.click()
                check_if_relevant()
        except Exception as e:
            continue