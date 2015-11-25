from bs4 import BeautifulSoup as bs
import urllib2
import json
import re
from datetime import datetime


class football_scraper:

    def __init__(self):
        url1 = (
            'http://www.scoresandodds.com/pfootballschedule_20140908_'
            '20180915_thisweek.html?sort=rot')
        try:
            soup = bs(urllib2.urlopen(url1).read(), 'html5lib')
        except:
            soup = bs(urllib2.urlopen(url1).read(), 'html5lib')

        q = soup.find(id='contents')
        w = q.find(class_='section')
        r = [i for i in w.contents if i != '\n']
        self.k = {}
        gd = None
        league = None

        for i in r:
            if 'class' in i.attrs:
                s = i.text.split()
                gd = s[0]
                league = s[1]
                if league not in self.k:
                    self.k[league] = {gd: []}
                else:
                    self.k[league][gd] = []
            else:
                self.k[league][gd] = self.make_games(i)

    def make_games(self, table):
        x = [i.parent for i in table.tbody.find_all(class_='teamName')]
        games = []
        away = None
        for m, i in enumerate(x):
            if m % 2 == 0:
                away = i.contents
            else:
                games.append(self.new_game(away, i.contents))
        return games

    def parse_it(self, a, h, ch, d):
        if 'PK' in [a, h]:
                d[ch + '_fav'] = 'Pick'
                d[ch + '_line'] = 0
                return d
        f = min(a, h)
        if f == '':
            f = max(a, h)
            if a == max(a, h):
                h = '99'
            else:
                a = '99'
        if a == min(a, h):
            d[ch + '_fav'] = d['away']
        else:
            d[ch + '_fav'] = d['home']

        try:
            f = float(f)
            d[ch + '_line'] = f
            d[ch + '_fav_vig'] = -110
        except ValueError:
            w = re.split('\s|o', f)
            try:
                d[ch + '_line'] = float(w[0])
            except ValueError:
                print w
                print f == ''
                print ch
                print d
            try:
                d[ch + '_fav_vig'] = float(w[1]) - 100
            except ValueError:
                if w[1] == 'EVEN':
                    d[ch + '_fav_vig'] = -100
        return d

    def new_game(self, away, home):
        d = {}
        d['away'] = away[1].text.strip()[4:]
        d['home'] = home[1].text.strip()[4:]
        a2 = away[2].text.strip()
        h2 = home[2].text.strip()
        a4 = away[4].text.strip()
        h4 = home[4].text.strip()
        # a5 = away[5].text.strip() //moneyline
        # h5 = home[5].text.strip() //moneyline
        if a2 == '':
            return d
        d = self.parse_it(a2, h2, 'o', d)
        d = self.parse_it(a4, h4, 'c', d)

        return d

    def to_json_file(self, direct='', stamp='', name='lines'):
        """write lines dictionary as json file

        Keyword Arguments:
        direct -- directory to put file in, root is active folder and program
        doesn't verify that directory exists or is valid. (default '')

        stamp -- last portion of file naming scheme (default '')
        name -- name of file (default 'lines')
        """
        with open('lines'+direct+'.json', 'w') as f:
            json.dump(
                self.k, f, sort_keys=True, indent=4, separators=(',', ': '))

    def to_json_string(self):
        return json.dumps(self.k)

    def print_it(self, league):
        """ prints lines of the given league, must be valid key in dict k"""
        for i in sorted([i for i in self.k[league]]):
            print i
            for j in self.k[league][i]:
                q = j['away'].title() + ' at ' + j['home'].title()
                if 'c_fav' in j:
                    g = j['c_fav'].title() + ' ' + str(j['c_line'])
                else:
                    g = 'no line'
                print q + ': ' + g

if __name__ == "__main__":
    scraper = football_scraper()
    scraper.print_it('NFL')
    scraper.to_json_file(direct=datetime.now().strftime("_%Y_%m_%d_%H_%M"))

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
