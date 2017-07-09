import pandas as pd
import requests
from bs4 import BeautifulSoup as bsoup
from urlparse import urlparse

def grab_first():
    for year in [2016, 2015, 2014, 2013]:
        for week in range(1,17):
            url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={0}&year={1}&game=fd&scsv=1'.format(week, year)
            html = requests.get(url)
            soup = bsoup(html.content)
            pre = soup.find_all('pre')
            with open('test.csv', 'a+') as f:
                for i in pre[0]:
                    f.write(str(i))
    f.close()
    return pre

if __name__ == '__main__':
    url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week=17&year=2016&game=fd&scsv=1'
    #
    # 'http://rotoguru1.com/cgi-bin/fyday.pl?week=17&year=2014&game=fd&scsv=1'
    # 'http://rotoguru1.com/cgi-bin/fyday.pl?week=16&year=2015&game=fd&scsv=1'
    soup = grab_first()
