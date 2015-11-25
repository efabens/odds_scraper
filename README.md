# odds_scraper

Scrapes for sports odds

scraper.py creates a dictionary of today's odds

football_scraper.py creates a dictionary of this weeks football odds

##Requirements
Python 2.7+ (Not 3 compatible, needs new url lib and print statements)
Beautiful Soup 4

##json format
Top level is League: NFL,CFB,CFL

2nd is date

3rd level is gameinfo

If odds are not available only 'home' and 'away' are included

Otherwise data fields include: away, home, favorite (fav), juice on favorite (fav_vig), line (line). The last three included twice and prefixed with either "c_" or "o_" for current or opening respectively.

I make no claims regarding the accuracy of this data and it should be used for informational and entertainment purposes only.

All data sourced and copywrite scoresandodds.com this script and its creator makes no
claim of ownership.
The activities offered by advertising links to other sites, may be deemed an
illegal activity in certain jurisdictions and are void where prohibited.
The viewer is specifically warned that they should make their own inquiry
into the legality of participating in any of these games and/or activities.
The owner of this web site assumes no responsibility for the actions by and
makes no representation or endorsement of any of these games and/or
activities if they are illegal in the jurisdiction of the reader or client of this site.
