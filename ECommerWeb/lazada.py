from selenium.common.exceptions import NoSuchElementException

class lazada:
    ecommer_web = "https://www.lazada.com.my/"
    ecommer_name = "Lazada"

    # return data as product name, price, URL, e-commerce brand
    def search_product(self, browser, product_name):
        print("Start searching {}".format(self.ecommer_name))

        data_list = []

        browser.get(self.ecommer_web)
        search_elem = browser.find_element_by_css_selector("#q")
        search_elem.send_keys(product_name)
        search_elem.submit()

        while True:
            product_list = browser.find_elements_by_css_selector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-20.ant-col-push-4.c1z9Ut > div.c1_t2i > div.c2prKC")
            print("Number of item {} in {}".format(len(product_list), self.ecommer_name))
        
            if(len(product_list) > 0):
                for product in product_list:    
                    product_title_content = product.text.split("\n")

                    product_name = product_title_content[0]
                    product_price = product_title_content[1]
                    product_url = product.find_element_by_tag_name("a").get_attribute("href")

                    data_list.append((product_name, product_price, product_url, self.ecommer_name))

            # Check have next page or not
            try:
                # Stop the search
                browser.find_element_by_css_selector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-20.ant-col-push-4.c1z9Ut > div.c3gNPq > div > ul > li.ant-pagination-disabled.ant-pagination-next")
                break
            except NoSuchElementException:
                # Continue search
                next_page_elem = browser.find_element_by_css_selector("#root > div > div.ant-row.c10-Cg > div.ant-col-24 > div > div.ant-col-20.ant-col-push-4.c1z9Ut > div.c3gNPq > div > ul > li.ant-pagination-next > a")
                next_page_elem.click()

        return data_list