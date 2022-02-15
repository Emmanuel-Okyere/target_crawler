from distutils.spawn import find_executable
from email import header
from gettext import find
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
import os 
from selenium.webdriver.common.by import By
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://www.target.com/")

print(driver.title)
driver.maximize_window()
container_nav  = driver.find_element(By.CSS_SELECTOR, 'a[data-lnk="C_Women_CN"]')
driver.implicitly_wait(30)
container_nav.click()
women_nav = driver.find_element(By.CSS_SELECTOR, 'a[data-lnk="C_Women\'sClothing_WEB-352660_0"]')
women_nav.click()
number_of_items = driver.find_element(By.CSS_SELECTOR,'button[type="button"][data-test="select"]').text
print(f"The total number of navigation(s) is: {number_of_items[-2:]}")
# getting_prod_in = driver.find_element_by_css_selector('div[data-test="productGridContainer"]').find_elements_by_css_selector('li[data-test="list-entry-product-card"]')
# print(getting_prod_in)
def save_data(product_list):
    data = pd.DataFrame(product_list, columns=['Product Name', "Product Price" ,"Product Description", "Product Link", "Product Image Link"])
    os.makedirs('WomenListFolderDec', exist_ok=True)  
    data.to_csv('WomenListFolderDec/women_clothes_data10.csv', mode='a', header = False)


for s in range(1,(int(number_of_items[-2:])+1)):
    for j in range(24):
        getting_prod = driver.find_element(By.CSS_SELECTOR,'div[data-test="productGridContainer"]').find_elements(By.CSS_SELECTOR, 'li[data-test="list-entry-product-card"]')
        print(j)
        print(len(getting_prod))
        scheight = .1
        while scheight < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
            scheight += .01
        try:
            a = getting_prod[j]
            for i in [a]:
                product_list = []
                time.sleep(20)
                driver.refresh
                i.find_element(By.CSS_SELECTOR, 'div[data-test="product-card-apparel-vertical"]').click()
                time.sleep(10)
                product_name = driver.find_element(By.CSS_SELECTOR, 'div[class="h-margin-v-tight h-padding-h-default"]').find_element(By.CSS_SELECTOR, 'h1[data-test="product-title"][itemprop="name"]').text
                product_price = driver.find_element(By.CSS_SELECTOR, 'span[data-test="product-price"]').text
                product_url = driver.current_url
                driver.find_element(By.CSS_SELECTOR, 'button[type="button"][data-test="toggleContentButton"]').click()
                # time.sleep(10)
                product_descriptions = driver.find_element(By.CSS_SELECTOR, 'div[data-test="item-details-description"]').text
                image_link = driver.find_element(By.CSS_SELECTOR, 'div[aria-hidden="false"][class="slide--active"]')
                new = image_link.find_element(By.TAG_NAME, "img").get_attribute("src")
                print(new)
                print(product_name)
                print(product_price)
                print(product_url)
                print(product_descriptions)
                product_list.append([product_name, product_price, product_descriptions, product_url, new])
                save_data(product_list)
                driver.back()
                time.sleep(10)

        except IndexError as err:
            print("Index Error Occured", err)
        except NoSuchElementException as err:
            print("No Such Element Error Occured", err)
        except StaleElementReferenceException as err:
            print("Stale Element Reference Error Occured", err)

        finally:
            pass                  
    print("Erroroorro")
    time.sleep(15)
    page_nav = driver.find_element(By.CSS_SELECTOR, 'div[data-test="pagination"]')
    new = page_nav.find_element(By.CSS_SELECTOR, 'a[type="button"][data-test="next"]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(15)
    new.click()
    print("************************Moving on to the next----"+str(s+1)+"********************")



driver.close()