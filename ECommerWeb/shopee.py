from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class shopee:
    ecommer_web = "https://shopee.com.my/"
    ecommer_name = "Shopee"

    # return data as product name, price, URL, e-commerce brand
    def search_product(self, browser, product_name):
        print("Start searching {}".format(self.ecommer_name))
        wait = WebDriverWait(browser, 15)

        data_list = []

        browser.get(self.ecommer_web)

        overlay_elem = browser.find_element_by_tag_name("body")
        overlay_elem.send_keys(Keys.ESCAPE)
        overlay_elem.send_keys(Keys.ESCAPE)
        search_elem = browser.find_element_by_css_selector("#main > div > div._1Bj1VS.qEcSbS > div:nth-child(1) > div > div.container-wrapper.header-with-search-wrapper > div > div.header-with-search__search-section > div.shopee-searchbar > div > form > input")
        search_elem.send_keys(product_name)

        search_button = browser.find_element_by_css_selector("#main > div > div._1Bj1VS.qEcSbS > div:nth-child(1) > div > div.container-wrapper.header-with-search-wrapper > div > div.header-with-search__search-section > div.shopee-searchbar > button")
        search_button.click()

        while True:
            product_list = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "#main > div > div._1Bj1VS > div.container._2_Y1cV > div.jrLh5s > div > div.row.shopee-search-item-result__items > div")))            
            print("Number of item {} in {}".format(len(product_list), self.ecommer_name))

            if(len(product_list) > 0):
                for product in product_list:  
                    if (not product.text):
                        product.location_once_scrolled_into_view
                        time.sleep(2)

                    product_title_content = product.text.split("\n")

                    product_name = product_title_content[0]
                    product_price = product_title_content[2]
                    product_url = product.find_element_by_tag_name("a").get_attribute("href")

                    data_list.append((product_name, product_price, product_url, self.ecommer_name))

            # Check have next page or not
            try:
                # Stop the search
                browser.find_element_by_css_selector("#main > div > div._1Bj1VS > div.container._2_Y1cV > div.jrLh5s > div > div.shopee-sort-bar > div.shopee-mini-page-controller > button.shopee-button-outline.shopee-mini-page-controller__next-btn.shopee-button-outline--disabled")
                print("end of page")
                break
            except NoSuchElementException:
                # Continue search
                next_page_elem = browser.find_element_by_css_selector("#main > div > div._1Bj1VS > div.container._2_Y1cV > div.jrLh5s > div > div.shopee-sort-bar > div.shopee-mini-page-controller > button.shopee-button-outline.shopee-mini-page-controller__next-btn")
                print("next page")
                next_page_elem.click()
            

        return data_list
        