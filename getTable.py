from bs4 import BeautifulSoup
import requests
import pandas as pd


def geturl(id):
    url = 'http://lexue.bit.edu.cn/mod/programming/reports/detail.php?id=' + str(id) + '&latestonly=1&lastinitial&firstinitial&group=6075&judgeresult&page=0&perpage=100'
    return url

def getData(id):
    headers = {'User-Agent': 'Useragent'}
    cookies = {'cookie': 'Cookies'}
    res = requests.get(geturl(id), cookies = cookies, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    tables = soup.select('table')
    df_list = []
    for table in tables:
        tmp = pd.concat(pd.read_html(table.prettify()))
        # tmp['全名'].replace(' ', '', regex = True, inplace = True)
        tmp['全名'] = tmp['全名'].str.replace(' ', '')
        df_list.append(tmp)
    df = pd.concat(df_list)
    df.to_excel('Data.xlsx')

if __name__ == '__main__':
    getData(130249)