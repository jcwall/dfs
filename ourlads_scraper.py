import pandas as pd
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib
import numpy as np

def get_dcharts(url, columns):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    table = soup.find("table")
    headings = [th.get_text().encode('utf-8')[-1:] for th in table.find('tr').find_all('th')]
    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text().encode('utf-8') for td in row.find_all("td")))
        datasets.append(dataset[::2])
    newsets = [i for i in datasets if i[0][1] in ['RWR', 'LWR', 'TE', 'RB', 'QB', 'FB', 'KR', 'PR']]
    head = soup.find('h1')
    team, date = head.attrs['class'][0], head.text[-11:-1]
    teamz = list(set([x[1] for i in newsets for x in i[1:]]))
    teamz.remove('')
    teamfin = [(i.split()[0] + ' ' + i.split()[1]) for i in teamz]
    df = pd.DataFrame(columns=columns, index=teamfin)
    df.team, df.week = team, date
    for i in teamz:
        for pos in newsets:
            for player in pos[1:]:
                if i == player[1]:
                    name = i.split()[0] + ' ' + i.split()[1]
                    df.loc[name, pos[0][1]] = player[0]
    df.fillna(0, inplace=True)
    #2 - 7 is offseason months
    df['offseason'] = df['week'].apply(lambda x: 1 if int(x[:2]) in range(2,8) else 0)
    df.index.name = 'name'
    df = df[df['offseason'] != 1]
    # df.drop('offseason', axis=1, inplace=True)
    return df

# def timed(f):
#   start = time.time()
#   ret = f()
#   elapsed = time.time() - start
#   print ret, elapsed

if __name__ == '__main__':
    columns = ['team', 'week', 'RWR', 'LWR', 'TE', 'RB', 'QB', 'FB', 'KR', 'PR']
    dfs = []
    teams = ['GB', 'BUF', 'MIA', 'NE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT', 'HOU', 'IND', 'JAX', 'TEN', 'DEN', 'KC', 'LAC', 'OAK', 'DAL', 'NYG', 'PHI', 'WAS', 'CHI', 'DET', 'MIN', 'ATL', 'CAR', 'NO', 'TB', 'ARZ', 'SF', 'SEA', 'LAR']
    for team in teams:
        for week in range(139, 197):
            #139 is first week of 2013
            url = 'http://www.ourlads.com/nfldepthcharts/archive/{1}/{0}'.format(team, week)
            try:
                dfs.append(get_dcharts(url, columns))
            except:
                pass
    findf = pd.concat(dfs)
