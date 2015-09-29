from bs4 import BeautifulSoup as bs
import urllib2
import json


class odd_scraper:

    def __init__(self):
        url1 = 'http://www.scoresandodds.com/pfootballschedule_20140908_20180915_thisweek.html?sort=rot'
        soup = bs(urllib2.urlopen(url1).read())

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
        f = min(a, h)
        if a == min(a, h):
            d[ch + '_fav'] = d['away']
        else:
            d[ch + '_fav'] = d['home']

        try:
            f = float(f)
            d[ch + '_line'] = f
            d[ch + '_fav_vig'] = -110
        except ValueError:
            if f == 'PK':
                d[ch + '_fav'] = 'Pick'
                d[ch + 'o_line'] = 0
            else:
                w = f.split(' ')
                d[ch + '_line'] = float(w[0])
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
        #a5 = away[5].text.strip() //moneyline
        #h5 = home[5].text.strip() //moneyline
        if a2 == '':
            return d
        d = self.parse_it(a2, h2, 'o', d)
        d = self.parse_it(a4, h4, 'c', d)

        return d

    def to_json_file(self, direct=''):
        with open(direct+'lines.json', 'w') as f:
            json.dump(self.k, f, sort_keys=True, indent=4,
                separators=(',', ': '))

    def to_json_string(self):
        return json.dumps(self.k)

if __name__ == "__main__":
    scraper = odd_scraper()


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
