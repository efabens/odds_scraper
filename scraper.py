from bs4 import BeautifulSoup as bs
import urllib2
import sys


def make_games(table):
    x = [i for i in table.tbody.find_all('tr') if i.attrs == {}]
    games = []
    a_game = None
    away = None
    for m, i in enumerate(x):
        if m % 2 == 0:
            a_game = {}
            away = i.contents
        else:
            games.append(new_game(away, i.contents))
    return games

def parse_it(a, h, ch, d):
    f=min(a,h)
    try:
        a = float(a)
        h = float(h)
        if a == max(a, h):
            d[ch+'_fav'] = d['home']
        else:
            d[ch+'_fav'] = d['away']
        d[ch+'_line'] = min(a, h)
    except ValueError:
        if a == 'PK' or h =='PK':
            d[ch+'_fav'] = 'Pick em'
            d[ch+'o_line'] = 0
        else:
            if a[0]=='-':
                try:
                    int(a)
                except Value
            print "Away", a
            print "home", h
    return d

def new_game(away, home):
    d = {}
    d['away'] = away[1].text.strip()[4:]
    d['home'] = home[1].text.strip()[4:]
    a2 = away[2].text.strip()
    h2 = home[2].text.strip()
    a4 = away[4].text.strip()
    h4 = home[4].text.strip()
    a5 = away[5].text.strip()
    h5 = home[5].text.strip()
    if a2 == '':
        return d
    d = parse_it(a2, h2, 'o', d)
    d = parse_it (a4, h4, 'c', d)

    return d

url1 = 'http://www.scoresandodds.com/pfootballschedule_20140908_20180915_thisweek.html?sort=rot'
soup = bs(urllib2.urlopen(url1).read())

q = soup.find(id='contents')
w = q.find(class_='section')
r = [i for i in w.contents if i != '\n']
k = {}
gd = None
league = None

for i in r:
    if 'class' in i.attrs:
        s = i.text.split()
        gd = s[0]
        league = s[1]
        if league not in k:
            k[league] = {gd: []}
        else:
            k[league][gd] = []
    else:
        k[league][gd] = make_games(i)


# All data sourced from scoresandodds.com this script and its creator makes no
# claim of ownership.
# The activities offered by advertising links to other sites, may be deemed an
# illegal activity in certain jurisdictions and are void where prohibited.
# The viewer is specifically warned that they should make their own inquiry
# into the legality of participating in any of these games and/or activities.
# The owner of this web site assumes no responsibility for the actions by and
# makes no representation or endorsement of any of these games and/or
# activities if they are illegal in the jurisdiction of the reader or client of
# this site.
