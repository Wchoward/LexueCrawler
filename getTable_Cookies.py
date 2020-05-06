from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
    

def geturl(id):
    url = 'http://lexue.bit.edu.cn/mod/programming/reports/detail.php?id=' + str(id) + '&latestonly=1&lastinitial&firstinitial&group=6075&judgeresult&page=0&perpage=100'
    return url

def getCookies(username, password):
    driver = webdriver.Chrome(executable_path = 'chromedriverPath')
    driver.get('http://lexue.bit.edu.cn/')
    driver.find_element('id', 'username').send_keys(username)
    driver.find_element('id', 'password').send_keys(password)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/form/ul/li[4]/input").click()
    cookies = driver.get_cookies()
    driver.close()
    return cookies

def getData(cookies, id):
    session = requests.Session()

    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    resp = session.get(geturl(id))
    soup = BeautifulSoup(resp.text, 'html.parser')
    tables = soup.select('table')
    df_list = []
    for table in tables:
        tmp = pd.concat(pd.read_html(table.prettify()))
        # tmp['全名'].replace(' ', '', regex = True, inplace = True)
        tmp['全名'] = tmp['全名'].str.replace(' ', '')
        df_list.append(tmp)
    df = pd.concat(df_list)
    df.to_excel(str(id) + '.xlsx')

if __name__ == '__main__':
    cookies = getCookies('username', 'password')
    getData(cookies, 130247)