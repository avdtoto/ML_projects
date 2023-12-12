import requests
from bs4 import BeautifulSoup
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from imdb_code import get_actors_by_movie_soup
from imdb_code import get_movies_by_actor_soup

# for one example
def helper_function_actor():
    url_actor = ' https://www.imdb.com/name/nm0425005/'

    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument(
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15")
    driver = webdriver.Chrome(options=options)

    driver.get(f"{url_actor}")

    wait = WebDriverWait(driver, 4)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span = 'See all']")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)

    soup_actor = BeautifulSoup(driver.page_source)
    actor_page = get_movies_by_actor_soup(soup_actor, 100)
    return actor_page

# for one example
def helper_function_cast():
    url_cast = 'https://www.imdb.com/title/tt3480822/fullcredits/'
    response = requests.get(url_cast)
    soup = BeautifulSoup(response.text)
    cast = get_actors_by_movie_soup(soup)
    return cast

cast = (helper_function_cast())
actor = (helper_function_actor())
print(len(cast))
print(len(actor))



