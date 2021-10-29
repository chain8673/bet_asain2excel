from selenium import webdriver
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from time import sleep
from lxml import etree
import requests

# 将浏览器隐藏
option = webdriver.ChromeOptions()
# option.add_argument('headless')  # 设置option
option.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
browser = webdriver.Chrome(options=option)


# 获取某一场比赛的地址
def getDetailUrl(url):
    browser.get(url)
    sleep(5)
    browser.refresh()
    sleep(5)
    browser.refresh()
    wait = WebDriverWait(browser, 10)  # 验证10秒之内，browser是否执行完成
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[10]/div[2]/div[3]/div[2]/table/tbody/tr[5]/td[9]/a[3]')))  # 等等ID为odds的元素出现
    tag = browser.find_element(By.XPATH, '/html/body/div[10]/div[2]/div[3]/div[2]/table/tbody/tr[5]/td[9]/a[3]')
    asainUrl = tag.get_attribute('href')
    browser.get(asainUrl)

    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="odds"]/tbody/tr[3]/td[12]/a[1]')))
    tag = browser.find_element(By.XPATH, '//*[@id="odds"]/tbody/tr[3]/td[12]/a[1]')
    aomenUrl = tag.get_attribute('href')
    browser.get(aomenUrl)
    return aomenUrl


def getData(url):
    homeTeam = browser.find_element(By.XPATH, '//*[@id="odds2"]/table/tbody/tr[1]/td[3]/b/font')
    awayTeam = browser.find_element(By.XPATH, '//*[@id="odds2"]/table/tbody/tr[1]/td[5]/b/font')
    response = requests.get(url)
    page_cont = response.content
    tree = etree.HTML(page_cont)
    trs = tree.xpath('//*[@id="odds2"]/table/tr')
    items = []
    for tr in trs[1:]:
        td_item = []
        td1 = tr.xpath('./td[1]//text()')[0]
        td2 = tr.xpath('./td[2]//text()')[0]
        td3 = tr.xpath('./td[3]//text()')[0]
        td4 = tr.xpath('./td[4]//text()')[0]
        td5 = tr.xpath('./td[5]//text()')[0]
        # td6 = tr.xpath('./td[6]//text()')[0]
        # td7 = tr.xpath('./td[7]//text()')[0]
        td_item.append(td1)
        td_item.append(td2)
        td_item.append(td3)
        td_item.append(td4)
        td_item.append(td5)
        # td_item.append(td6)
        # td_item.append(td7)
        print(td_item)
        items.append(td_item)

    print(items)


def main():
    print('I am main.')
    url = 'http://zq.win007.com/cn/SubLeague/60.html'
    aomenUrl = getDetailUrl(url)
    getData(aomenUrl)
    browser.close()


if __name__ == '__main__':
    main()
