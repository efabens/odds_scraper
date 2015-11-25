from bs4 import BeautifulSoup as bs
import urllib2
import json
import re
from datetime import datetime


class odd_scraper:

    def __init__(self):
        d = datetime.now().strftime("%Y%m%d")
        url1 = 'http://www.scoresandodds.com/pgrid_%s.html?sort=rot' % d

        try:
            soup = bs(urllib2.urlopen(url1).read(), 'html5lib')
        except:
            soup = bs(urllib2.urlopen(url1).read())

        q = soup.find(id='contents')
        w = q.find_all(class_='section')
        self.k = {}
        gd = None
        league = None

        for i in w:
            league = i.find(class_='league').text
            gd = i.find(class_='date').text
            if league not in self.k:
                self.k[league] = {gd: []}
            else:
                self.k[league][gd] = []
            self.k[league][gd] = self.make_games(i.find('table'))

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
        d['away'] = re.match("\d+ ([a-zA-Z ]*)", (away[0].text)).group(1)
        d['home'] = re.match("\d+ ([a-zA-Z ]*)", (home[0].text)).group(1)
        away_op = away[1].text.strip()
        home_op = home[1].text.strip()
        away_cur = away[3].text.strip()
        home_cur = home[3].text.strip()
        # a5 = away[5].text.strip() //moneyline
        # h5 = home[5].text.strip() //moneyline
        if away_op == '':
            return d
        d = self.parse_it(away_op, home_op, 'o', d)
        d = self.parse_it(away_cur, home_cur, 'c', d)

        return d

    def to_json_file(self, direct=''):
        with open('lines' + direct + '.json', 'w') as f:
            json.dump(
                self.k, f, sort_keys=True, indent=4,
                separators=(',', ': '))

    def to_json_string(self):
        return json.dumps(self.k)

    def print_it(self, league):
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
    scraper = odd_scraper()
    scraper.print_it('NBA')
    scraper.to_json_file(direct=datetime.now().strftime("%Y_%m_%d_%H_%m"))


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
