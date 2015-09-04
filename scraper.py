from bs4 import BeautifulSoup as bs
import urllib2
url1 = 'https://www.sportsinsights.com/free-odds/'
t = urllib2.Request(url1,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'})
#soup = bs(t.read())