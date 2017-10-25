from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from Crawling.mk_data import mk_data
from pyvirtualdisplay import Display


class Crawl():
    def __init__(self, MID):
        self.MID_URL = 'http://shopping.naver.com/detail/detail.nhn?nv_mid=' + MID
        self.MID = MID
        self.valid = False
        self.data_list = []

    def main(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Firefox(log_path='/home/pi/Django/geckodriver.log')
        driver.get(self.MID_URL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            valid_txt = str(soup.find('h3').find(text=True))
            if '판매중단' in valid_txt:
                self.valid = True
        except:
            try:
                valid_txt = soup.find_all('h2')[3].find(text=True)
                if '상품이' in valid_txt:
                    self.valid = True
            except:
                self.valid = False

        if not self.valid:
            try:
                option_list = soup.find_all('div', class_='condition_group')[1].findChildren(recursive=False)[
                    1].findChildren(recursive=False)
                wait = ui.WebDriverWait(driver, 10)
                for i in range(2, option_list.__len__() + 1):
                    driver.get(self.MID_URL)
                    option_name = str(
                        option_list[i - 1].findChildren(recursive=False)[2].findChildren(recursive=False)[1].find(
                            text=True))

                    xpath = '//*[@id="section_price"]/div[2]/div[2]/ul/li[' + str(i) + ']'
                    element = driver.find_element_by_xpath(xpath)
                    driver.execute_script("arguments[0].click();", element)
                    wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="section_price_list"]/table[2]'))

                    source_1 = driver.page_source
                    driver.find_element_by_xpath('//*[@id="section_price"]/div[2]/div[1]/div[2]/span[1]/a').click()
                    source_2 = driver.page_source
                    data = mk_data(source_1, source_2, self.MID, option_name, self.valid)
                    data.make()
                    self.data_list.append(data.data.__dict__)
            except:
                source_1 = driver.page_source
                driver.find_element_by_xpath('//*[@id="section_price"]/div[2]/div[1]/div[2]/span[1]/a').click()
                source_2 = driver.page_source
                data = mk_data(source_1, source_2, self.MID, '', self.valid)
                data.make()
                self.data_list.append(data.data.__dict__)

        else:
            data = mk_data('', '', self.MID, '', self.valid)
            data.make()
            self.data_list.append(data.data.__dict__)

        driver.close()
        display.popen.kill()
