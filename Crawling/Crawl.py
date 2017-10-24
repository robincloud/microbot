from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
from Crawling.mk_data import mk_data



def main():
    driver = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
    driver.get('http://shopping.naver.com/detail/detail.nhn?nv_mid=5639964597')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data_list = []
    try:
        option_list = soup.find_all('div', class_='condition_group')[1].findChildren(recursive=False)[1].findChildren(recursive=False)
        wait = ui.WebDriverWait(driver, 10)
        for i in range(2,option_list.__len__() + 1):
            driver.get('http://shopping.naver.com/detail/detail.nhn?nv_mid=5639964597')
            option_name = str(option_list[i - 1].findChildren(recursive=False)[2].findChildren(recursive=False)[1].find(text=True))

            xpath = '//*[@id="section_price"]/div[2]/div[2]/ul/li[' + str(i) + ']'
            element = driver.find_element_by_xpath(xpath)
            driver.execute_script("arguments[0].click();", element)
            wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="section_price_list"]/table[2]'))

            source_1 = driver.page_source
            driver.find_element_by_xpath('//*[@id="section_price"]/div[2]/div[1]/div[2]/span[1]/a').click()
            source_2 = driver.page_source
            data = mk_data(source_1, source_2, '5639964597', option_name)
            data.make()
            data_list.append(data.data.__dict__)
    except:
        source_1 = driver.page_source
        driver.find_element_by_xpath('//*[@id="section_price"]/div[2]/div[1]/div[2]/span[1]/a').click()
        source_2 = driver.page_source
        data = mk_data(source_1, source_2, '5639964597', '')
        data.make()
        data_list.append(data.data.__dict__)




if __name__ == '__main__':
    main()