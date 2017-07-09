import pandas as pd
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib

def clean_df():
    df = pd.read_csv('test.csv', sep=';')
    df = df[df.Week != 'Week']
    df['LWR_depth'], df['RWR_depth'], df['TE_depth'], df['RB_depth'], df['QB_depth'], df['FB_depth'], df['KR_depth'], df['PR_depth']= 0, 0, 0, 0, 0, 0, 0, 0
    df['Year'], df['Week'] = df['Year'].astype(int), df['Week'].astype(int)
    df['FD points'].fillna(0)
    df['FD points'] = df['FD points'].astype(float)
    df['FD salary'].fillna(0)
    df['FD salary'] = df['FD salary'].astype(float)
    return df

def filt_names():
    pass

if __name__ == '__main__':
    df = clean_df()
    url = 'http://www.ourlads.com/nfldepthcharts/archive/187/GB'
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    table = soup.find("table")
    headings = [th.get_text().encode('utf-8')[-1:] for th in table.find('tr').find_all('th')]
    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text().encode('utf-8') for td in row.find_all("td")))
        datasets.append(dataset[::2])
    newsets = [i for i in datasets if i[0][1] in ['RWR', 'LWR', 'TE', 'RB', 'QB', 'FB', 'KR', 'PR']]



#only keep wr, te, rb, qb, fb, kr, pr
# for pos in datasets:
#     for player in pos:
#         df[]
